$(document).ready(function() {
    
    /*
     * Reusablity hint:
     *
     *  Set the directions you also have in your urls.py. Order is
     *  0: up vote; 1: down vote; 2: clear vote
     *
     *  The rest should work out of the box without modification.
     */
    var validDirections = ['upvote', 'downvote', 'clearvote'];
    
    /*
     * Get the direction out of a url
     */
    function getDirectionFromURL(url) {
        for (var i = 0; i < validDirections.length; i++) {
            if (url.match(validDirections[i])) {
                return validDirections[i];
            }
        }
    }
    
    /*
     * Set a new direction in a url
     */
    function setNewDirectionURL(url, direction) {
        for (var i = 0; i < validDirections.length; i++) {
            if (url.match(validDirections[i])) {
                return url.replace(validDirections[i], direction);
            }
        }
    }
    
    /*
     * We swap this function out of the updateBadge function.
     * Add some shine when updateing the score.
     */
    function updateScore(target, score) {
        target.text(score);
    }
    
    /*
     * Updates the badge: the URL of the arrows, the class of the arrows
     * that marks the active one and the score
     */
    function updateBadge(vote_badge, current_form, value) {
        
        // Get the direction from the currently clicked form. Can be either
        // up, down or clear.
        direction = getDirectionFromURL(current_form.attr('action'));
        
        // Update the score
        updateScore(vote_badge.find('span.score'), value);
        
        // Set both arrows to inactive
        vote_badge.find('input[type=submit]').removeClass('active');
        
        // If we don't clicked on an clear-arrow, mark it active
        if (direction != validDirections[2]) {
            current_form.find('input[type=submit]').addClass('active');
        }
        
        /*
         * This function .... works. :o)
         */
        // Upvote
        if (direction == validDirections[0]) {
            vote_badge.find('form.upform').attr('action', setNewDirectionURL(vote_badge.find('form.upform').attr('action'), validDirections[0]));
            vote_badge.find('form.downform').attr('action', setNewDirectionURL(vote_badge.find('form.downform').attr('action'), validDirections[2]));
        }
        // Downvote
        else if (direction == validDirections[1]) {
            vote_badge.find('form.upform').attr('action', setNewDirectionURL(vote_badge.find('form.upform').attr('action'), validDirections[2]));
            vote_badge.find('form.downform').attr('action', setNewDirectionURL(vote_badge.find('form.downform').attr('action'), validDirections[1]));
        }
        // Clearvote
        else {
            vote_badge.find('form.upform').attr('action', setNewDirectionURL(vote_badge.find('form.upform').attr('action'), validDirections[0]));
            vote_badge.find('form.downform').attr('action', setNewDirectionURL(vote_badge.find('form.downform').attr('action'), validDirections[1]));
        }
    }
    
    /*
     * Iterate over vote forms, if one is submitted, call the form-url via
     * POST and update the score, urls and arrow styles.
     */
    $("div.vote_badge").each(function() {
        // Remember this badge.
        var vote_badge = $(this);
        
        // Iterate over forms
        $(this).find("form").each(function() {
            
            // Bind updateBadge function to all forms
            var current_form = $(this);
            $(this).submit(function() {
                var update_url = $(this).attr('action');
                console.log(this);
                // Do a post request and do something with the (json) response
                $.post(update_url, $(this).serialize(), function(response) {
                    if (response.success) {
                        // Update the score count
                        updateBadge(vote_badge, current_form, response.score.score)
                    }
                    else {
                        // Silent error
                        console.log('Got no valid response from the voting app');
                        console.log(response);
                    }
                }, 'json');
                return false;
            });
        });
    });
});