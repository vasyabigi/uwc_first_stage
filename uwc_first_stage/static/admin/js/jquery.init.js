// Puts the included jQuery into our own namespace
var django = {
    "jQuery": jQuery.noConflict(true)
};
var $ = django.jQuery;
var jQuery = $;
