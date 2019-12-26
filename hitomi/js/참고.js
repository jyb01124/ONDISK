var query = "korean"
var separator = '-';
var extension = '.html';
var galleriesdir = 'galleries';
var index_dir = 'tagindex';
var galleries_index_dir = 'galleriesindex';
const max_node_size = 464;
const B = 16;
var search_serial = 0;
var search_result_index = -1;
const compressed_nozomi_prefix = 'n';
var domain = "ltn.hitomi.la";

$(function() {
    get_index_version('galleriesindex').then((string) => {
            galleries_index_version = string;
            do_search();
    });
});

function get_index_version(name) {
    return new Promise((resolve, reject) => {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '//'+domain+'/'+name+'/version?_='+(new Date).getTime());
            xhr.onreadystatechange = function(oEvent) {
                    if (xhr.readyState === 4) {
                            let retval = 'failed';
                            if (xhr.status === 200) {
                                    retval = xhr.responseText;
                            }
                            resolve(retval);
                    }
            };
            xhr.send();
    });
}

function do_search() {
    start_loading_timer();
    
    let query_string = decodeURIComponent(window.location.search).replace(/^\?/, '');
    
    if (!query_string.match(/[^A-Za-z0-9_: .-]/)) { //can't put other characters back into the page due to xss (20150110)
            $('#query-input').val(query_string);
    }
    
    let terms = query_string.toLowerCase().trim().split(/\s+/);
    let positive_terms = [], negative_terms = [];
    
    $.each(terms, function(i, term) {
        term = term.replace(/_/g, ' ');
            if (term.match(/^-/)) {
                    negative_terms.push(term.replace(/^-/, ''));
            } else {
                    positive_terms.push(term);
            }
    });
    

    new Promise((resolve, reject) => { //first results
            if (!positive_terms.length) {
                    get_galleryids_from_nozomi(undefined, 'index', 'all').then(new_results => {
                            results = new_results;
                            resolve();
                    });
            } else {
                    const term = positive_terms.shift();
                    get_galleryids_for_query(term).then(new_results => {
                            results = new_results;
                            resolve();
                    });
            }
    }).then(() => { //positive results
            return Promise.all(positive_terms.map(term => {
                    return new Promise((resolve, reject) => {
                            get_galleryids_for_query(term).then(new_results => {
                                    const new_results_set = new Set(new_results);
                                    results = results.filter(galleryid => new_results_set.has(galleryid));
                                    resolve();
                            });
                    });
            }));
    }).then(() => { //negative results
            return Promise.all(negative_terms.map(term => {
                    return new Promise((resolve, reject) => {
                            get_galleryids_for_query(term).then(new_results => {
                                    const new_results_set = new Set(new_results);
                                    results = results.filter(galleryid => !new_results_set.has(galleryid));
                                    resolve();
                            });
                    });
            }));
    }).then(() => {
            const final_results_length = results.length;
            $('#number-of-results').html(final_results_length);
            if (!final_results_length) {
                    hide_loading();
                    $('.gallery-content').html($('#no-results-content').html());
            } else {
                    put_results_on_page();
            }
    });
}

var get_galleryids_for_query = function(query) {
    return new Promise((resolve, reject) => {
            query = query.replace(/_/g, ' ');
            
            if (query.indexOf(':') > -1) {
                    const sides = query.split(/:/);
                    const ns = sides[0];
                    let tag = sides[1];
                    
                    let area = ns;
                    let language = 'all';
                    if ('female' === ns || 'male' === ns) {
                            area = 'tag';
                            tag = query;
                    } else if ('language' === ns) {
                            area = undefined;
                            language = tag;
                            tag = 'index';
                    }
                    
                    get_galleryids_from_nozomi(area, tag, language).then(resolve);
                    
                    return;
            }
            
            const key = hash_term(query);
            const field = 'galleries';
    
            get_node_at_address(field, 0).then((node) => {
                    if (!node) {
                            resolve([]);
                            return;
                    }
                    
                    B_search(field, key, node).then((data) => {
                            if (!data) {
                                    resolve([]);
                                    return;
                            }
                            
                            get_galleryids_from_data(data).then(resolve);
                    });
            });
    });
};

var hash_term = function(term) {
    return new Uint8Array(sha256.array(term).slice(0, 4));
};

var get_node_at_address = function(field, address, serial) {
    return new Promise((resolve, reject) => {
            if (serial && serial !== search_serial) { //outdated request
                    resolve();
                    return;
            }
            
            let url = '//'+domain+'/'+index_dir+'/'+field+'.'+tag_index_version+'.index';
            if (field === 'galleries') {
                    url = '//'+domain+'/'+galleries_index_dir+'/galleries.'+galleries_index_version+'.index';
            }
            get_url_at_range(url, [address, address+max_node_size-1]).then((nodedata) => {
                    if (nodedata) {
                            resolve(decode_node(nodedata));
                    } else {
                            resolve();
                    }
            });
    });
};

function get_url_at_range(url, range) {
    return new Promise((resolve, reject) => {
            retry(() => {
                    return new Promise((resolve, reject) => {
                            var xhr = new XMLHttpRequest();
                            xhr.open('GET', url);
                            xhr.responseType = 'arraybuffer';
                            xhr.setRequestHeader('Range', 'bytes='+range[0].toString()+'-'+range[1].toString());
                            xhr.onreadystatechange = function(oEvent) {
                                    if (xhr.readyState === 4) {
                                            if (xhr.status === 200 || xhr.status === 206) {
                                                    resolve(new Uint8Array(xhr.response));
                                            } else {
                                                    reject(new Error(`get_url_at_range(${url}, ${range}) failed, xhr.status: ${xhr.status}`));
                                            }
                                    }
                            };
                            xhr.send();
                    });
            }).then(resolve).catch(console.error);
    });
}

var B_search = function(field, key, node, serial) {
    return new Promise((resolve, reject) => {
            let compare_arraybuffers = function(dv1, dv2) {
                    const top = Math.min(dv1.byteLength, dv2.byteLength);
                    for (let i = 0; i < top; i++) {
                            if (dv1[i] < dv2[i]) {
                                    return -1;
                            } else if (dv1[i] > dv2[i]) {
                                    return 1;
                            }
                    }
                    return 0;
            };
    
            let locate_key = function(key, node) {
                    let cmp_result = -1;
                    let i;
                    for (i = 0; i < node.keys.length; i++) {
                            cmp_result = compare_arraybuffers(key, node.keys[i]);
                            if (cmp_result <= 0) {
                                    break;
                            }
                    }
                    return [!cmp_result, i];
            };
    
            let is_leaf = function(node) {
                    for (let i = 0; i < node.subnode_addresses.length; i++) {
                            if (node.subnode_addresses[i]) {
                                    return false;
                            }
                    }
                    return true;
            };
            
            
            if (!node) {
                    resolve(false);
                    return;
            }


            if (!node.keys.length) { //special case for empty root
                    resolve(false);
                    return;
            }
    
            let [there, where] = locate_key(key, node);
            if (there) {
                    resolve(node.datas[where]);
                    return;
            } else if (is_leaf(node)) {
                    resolve(false);
                    return;
            }
    
            //it's in a subnode
            get_node_at_address(field, node.subnode_addresses[where], serial).then((node) => {
                    B_search(field, key, node, serial).then(resolve);
            });
    });
};