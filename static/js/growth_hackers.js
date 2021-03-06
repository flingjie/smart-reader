Vue.config.delimiters = ['[[', ']]'];

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

$(document).ready(function() {
    new Vue({
        el:'#content',
        ready: function() {
            var category = $.cookie('category') || 'new';
            this.$set('category', category)
            this.get_post();
        },
        data: {
            posts: [],
            cur_page: null,
            page_list: [],
            total_page: null,
            category: 'new',
        },
        methods: {
            get_post: function(data){
                this.$set('cur_page', getUrlParameter('page'));
                var post_data = {
                    category: this.category,
                    page: this.cur_page
                };
                this.$http.post('/posts', post_data).then((response) => {
                    var data = JSON.parse(response.data);
                    this.$set("posts", data.posts);
                    this.$set('cur_page', data.cur_page);
                    this.$set('page_list', data.page_list);
                    this.$set('total_page', data.total_page);
                  }, (response) => {
                    console.log(response.data);
                  });
            },
            mark_all_read: function(obj_id){
                var ids = [];
                for(var i=0;i<this.posts.length;i++){
                    ids.push(this.posts[i]._id['$oid']);
                }
                var post_data = {
                    ids: ids,
                    category: this.category,
                    page: this.cur_page
                }
                this.$http.post('/mark_all_read',
                    post_data).then((response) => {
                        var data = JSON.parse(response.data);
                        this.$set("posts", data.posts);
                        this.$set('cur_page', data.cur_page);
                        this.$set('page_list', data.page_list);
                        this.$set('total_page', data.total_page);
                      }, (response) => {
                        console.log(response.data);
                      });
            },
            mark_visit: function(obj_id, e){
                this.$http.post('/mark_visit',
                    {obj_id: obj_id}).then((response) => {
                        $(e.target).addClass('positive');
                  }, (response) => {
                    console.log(response.data);
                  });
            },
            change_category: function(category, e){
                this.$set('category', category);
                $.cookie('category', this.category,  {path: '/'});
                $(e.target)
                     .addClass('active')
                     .closest('.ui.menu')
                     .find('.item')
                     .not($(e.target))
                     .removeClass('active');
                this.get_post();
            },
            on_enter: function(e){
                $(e.target).addClass('warning');
            },
            on_leave: function(e){
                $(e.target).removeClass('warning');
            },
        }
    });
});