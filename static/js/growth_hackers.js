Vue.config.delimiters = ['[[', ']]'];

$(document).ready(function() {
    new Vue({
        el:'#content',
        ready: function() {
            this.$http.get('/posts').then((response) => {
                    var data = JSON.parse(response.data);
                    this.$set("posts", data['posts']);
                    this.$set("page_list", data['page_list']);
                  }, (response) => {
                    console.log(response.data);
                  });
        },
        data: {
            posts: [],
        },
        methods: {
            mark_read: function(title){
                this.$http.post('/mark_read',
                    {title: title}).then((response) => {
                    this.$set("posts", response.data);
                  }, (response) => {
                    console.log(response.data);
                  });
            }
        }
    });
});