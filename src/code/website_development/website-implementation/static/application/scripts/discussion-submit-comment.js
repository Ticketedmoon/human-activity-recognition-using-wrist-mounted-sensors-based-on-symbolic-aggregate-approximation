$(document).ready(function(){
    $("#submission-button").click(function () {
        console.log("Button Pushed")
        var user_name = $('#name').val();
        var comment_desc = $('#bio').val();
        
        $.ajax({
            url: '/comments/validate_comment/',
            data: {
                'username': user_name,
                'comment_description' : comment_desc
            },
            dataType: 'json',
            success: function (data) {
                console.log("Comment Successful");
            }
        });
    });
});