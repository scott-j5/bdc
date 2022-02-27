import LOAD from './load.js';

BLOGLIST = {
    searchQuery: "",
    searchSelector: "",
    tagListSelector: "",
    windowSelector: "",

    //Set Listeners for filter inputs
    //Runs render on tags/ search input
    init: function(searchSelector, tagListSelector, windowSelector){
        this.update();

        this.searchSelector = searchSelector;
        this.tagListSelector = tagListSelector;
        this.windowSelector = windowSelector;

        document.querySelector(searchSelector).addEventListener("keyup", BLOGLIST.searchDelay(function(e){BLOGLIST.search(e)}, 500));
        document.querySelectorAll(tagListSelector).forEach(item => {
            item.children.forEach(listItem => {
                listItem.addEventListener("click", BLOGLIST.updateTags);
            });
        });
        BLOGLIST.setPageListeners();
    },
    update: function(){
        this.getQuery();
        this.load();
        this.renderSearchInput();
        this.renderTags();
    },
    //Populates existing filter params from GET request
    getQuery: function(){
        params = new URLSearchParams(window.location.search);
        // If GET contains params populate search query else set to defaults
        if(Array.from(params).length >= 1 ){
            tags = []
            if(params.get('tags')){
                params.get('tags').split(',').forEach(tag =>{
                    if(tag.length >= 1 && !isNaN(tag)){
                        tags.push(tag);
                    }
                });
            }
            this.searchQuery = {"search":(params.get('search') || ""), "tags": tags, "page": (params.get('page')|| 1)};
        }else{
            this.searchQuery = {"search":"", "tags": [], "page": 1}
        }
    },
    //Updates search string in searchQuery, loads updated content
    search: function(e){
        BLOGLIST.searchQuery.search = e.target.value;
        BLOGLIST.searchQuery.page = 1;
        BLOGLIST.load(true);
    },
    //Change page number
    togglePage: function(e){
        e.preventDefault();
        BLOGLIST.searchQuery.page = e.target.dataset.page;
        BLOGLIST.load(true);
        e.stopPropagation();
    },
    //Update the value of search input box
    renderSearchInput: function(){
        document.querySelector(BLOGLIST.searchSelector).value = BLOGLIST.searchQuery.search;
    },
    searchDelay: function(callback, ms){
        var timer = 0;
        return function() {
            var context = this, args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function () {
                callback.apply(context, args);
            }, ms || 0);
        };
    },
    updateTags: function(e){
        //If clicked tag is not in list, add it and add its css flag. else deactivate it
        if(! BLOGLIST.searchQuery.tags.includes(e.currentTarget.dataset.identifier)){
            BLOGLIST.searchQuery.tags.push(e.currentTarget.dataset.identifier);
        }else{
            BLOGLIST.searchQuery.tags = BLOGLIST.searchQuery.tags.filter(function(f){ return f !== e.currentTarget.dataset.identifier});
        }
        BLOGLIST.searchQuery.page = 1;
        BLOGLIST.renderTags();
        BLOGLIST.load(true);
    },
    renderTags: function(){
        //If there is active tags add active flag to ul element
        if(BLOGLIST.searchQuery.tags.length >= 1){
            document.querySelectorAll(BLOGLIST.tagListSelector).forEach(item => {
                item.classList.add('tag-list-active');
            });
        }else{
            document.querySelectorAll(BLOGLIST.tagListSelector).forEach(item => {
                item.classList.remove('tag-list-active');
            });
        }
        document.querySelectorAll(BLOGLIST.tagListSelector).children.forEach(item => {
            if(BLOGLIST.searchQuery.tags.includes(item.dataset.identifier)){
                item.classList.add("active");
            }else{
                item.classList.remove("active");
            }
        });
    },
    load: async function(pushState=null){
        var load = LOAD;
        var args = Object.keys(BLOGLIST.searchQuery).map(function(key) {
            return key + '=' + encodeURIComponent(BLOGLIST.searchQuery[key]);
          }).join('&');
        if(pushState){
            history.pushState(null, "", "?" + args)
        }
        var url = window.location.protocol + "//" + window.location.host + "/blogs/?" + args
        var element = document.querySelector(BLOGLIST.windowSelector);
        await load.loadToElement(element, url, 'text/html');
        BLOGLIST.setPageListeners();
    },
    setPageListeners: function(){
        document.querySelectorAll('.page-toggle').forEach(item => {
            item.addEventListener("click", BLOGLIST.togglePage);
        });
    },
}

export const blogList = function(
    searchSelector,
    tagListSelector,
    windowSelector
){
    var obj = BLOGLIST;
    obj.init(searchSelector, tagListSelector, windowSelector);

    window.onpopstate = function(e){
        obj.update();
    };
};