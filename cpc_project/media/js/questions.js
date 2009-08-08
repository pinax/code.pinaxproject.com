$("li.mark_as_accepted > a").click(function() {
    $.get(this.href);
    $(".accepted").removeClass("accepted");
    response = $(this).parents("div.response");
    response.addClass("accepted");
    return false;
});