$("li.mark_as_accepted > a").click(function() {
    $(".accepted").removeClass("accepted");
    response = $(this).parents("div.response");
    response.addClass("accepted");
    return false;
});