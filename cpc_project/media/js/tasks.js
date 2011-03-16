$(document).ready(function() {
    $('.task_grouping .toggle').toggle(
        function() {
            $(this).parents("tbody").next("tbody").hide();
            $(this).find('.arrow').html("&#x25B8;");
        }, 
        function() {
            $(this).parents("tbody").next("tbody").show();
            $(this).find('.arrow').html("&#x25BE;");
        }
    );
    $('.expand_all').click(function () {
        $('.task_group').show();
        $('.arrow').html("&#x25BE;");
    });
    $('.collapse_all').click(function () {
        $('.task_group').hide();
        $('.arrow').html("&#x25B8;");
    });
    $(".select_all").click(function () {
        $(this).closest("ul").find("input[type=checkbox]").attr("checked", "checked");
        return false;
    });
    $(".select_none").click(function () {
        $(this).closest("ul").find("input[type=checkbox]").attr("checked", "");
        return false;
    });
});