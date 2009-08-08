$("li.mark_as_accepted > a").click(function() {
    var anchor = $(this);
    $.post(this.href, function() {
        $(".accepted").removeClass("accepted");
        response = anchor.parents("div.response");
        response.addClass("accepted");
    });
    return false;
});