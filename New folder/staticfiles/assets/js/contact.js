$(document).ready(function(){
    
    (function($) {
        "use strict";

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2
                },
                subject: {
                    required: true,
                    minlength: 4
                },
                number: {
                    required: true,
                    minlength: 5
                },
                email: {
                    required: true,
                    email: true
                },
                message: {
                    required: true,
                    minlength: 20
                }
            },
            messages: {
                name: {
                    required: "You Must Enter Your Name",
                    minlength: "your name must consist of at least 2 characters"
                },
                subject: {
                    required: "You Must Write A Subject",
                    minlength: "your subject must consist of at least 4 characters"
                },
                number: {
                    required: "You Must Enter Your Number",
                    minlength: "your Number must consist of at least 5 characters"
                },
                email: {
                    required: "Enter Emial"
                },
                message: {
                    required: "You have to write something to send this form.",
                    minlength: "thats all?"
                }
            },
 
        })
    })
        
 })(jQuery)
})