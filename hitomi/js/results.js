"use strict";

var results_array = {}, results = [];
var results_per_page = 25;
var outstanding_requests = {};
var number_of_outstanding_requests = 0;


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


function get_block(url) {
        $.get(url, function(data, status) {
                if (status === 'success') {
                        delete outstanding_requests[url];
                        --number_of_outstanding_requests;
                        results_array[url] = data;
                        put_results_on_page();
                }
        });
}

function put_results_on_page() {
        $('.gallery-content').html('');
        
        var page_number = 1;
        var hash = document.location.hash.replace(/^#/, '');
        if (hash.length) {
                page_number = parseInt(hash);
        }
        
        var final_results_length = results.length;
        var number_of_pages = Math.ceil(final_results_length/results_per_page);
        var last_page_number = number_of_pages;
        
        var datas = [];
        for (var i = (page_number-1)*results_per_page; i < page_number*results_per_page && i < final_results_length; ++i) {
        	var result = results[i];
                var url = '//'+domain+'/'+galleryblockdir+'/'+result+extension;
                if (results_array[url]) {
                        datas.push(results_array[url]);
                        continue;
                }
                if (!outstanding_requests[url]) {
                        outstanding_requests[url] = 1;
                        ++number_of_outstanding_requests;
                        get_block(url); //calling a function is REQUIRED to give url its own scope
                }
        }
        if (number_of_outstanding_requests) return;
        
        hide_loading();
        $('.gallery-content').html(datas.join(''));
        moveimages();
        localDates();
        limitLists();
        
        insert_paging('#', '', '', page_number, last_page_number);
        scroll_to_top();
}

$(window).bind('hashchange', function() {
        start_loading_timer();
        put_results_on_page();
});

$(function() {
        get_index_version('galleriesindex').then((string) => {
                galleries_index_version = string;
                do_search();
        });
});
