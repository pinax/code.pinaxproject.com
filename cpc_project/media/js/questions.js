$("a.mark_as_accepted").click(function() {
    $(".accepted").removeClass("accepted");
    response = $(this).parents("div.response");
    response.addClass("accepted");
    return false;
});