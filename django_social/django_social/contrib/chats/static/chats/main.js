$(function(){

    $("#chat_form").submit(function(e) {
        e.preventDefault();
        send_message(this);
        return false;
    });

    $("#older_messages_loader").click(function(e) {
        e.preventDefault();
        get_previous_messages();
        return false;
    });


    function get_previous_messages() {
        var first_message_id = $("#message_box").data("firstMessageId");
        var load_messages_url = $("#message_box").data("loadMessagesUrl");
        load_messages("backward", first_message_id, 5, load_messages_url, handle_loaded_messages);
    }

    function sync_messages() {
        var $message_box = $("#message_box");
        var last_message_id = $message_box.data("lastMessageId");
        var load_messages_url = $message_box.data("loadMessagesUrl");
        if (last_message_id !== 0) {
            $message_box.data("lastMessageId", 0);
            load_messages("forward", last_message_id, 5, load_messages_url, handle_loaded_messages);
        }
    }


    /**
     * Represents a message.
     * @constructor
     * @param {string} type
     * @param {string} author
     * @param {string} message
     * @param {string} date
     * @param {string} file
     */
    function Message(type, author, message, date, file_name, file_url) {
        this.type = type;
        this.author = author;
        this.message = message;
        this.date = date;
        this.file_name = file_name;
        this.file_url = file_url;

        this.create_dom_element = function() {
            if (this.type === 'f') {
                return $("<div class=\"message file\">[" + this.date + '] ' + this.author + ':' +
                    this.message + " <a href=" + this.file_url + ">" + this.file_name + "</a></div>");
            }
            else {
                return $("<div class=\"message\">[" + this.date + '] ' + this.author + ':' + this.message + "</div>");
            }
        };
    }


    /**
     * handle_loaded_messages handles the response from `load_messages` function.
     *
     * @callback handle_loaded_messages
     * @param {String} direction - According to the dirrection, the function decides either to prepend or append the result
     * @param {Number} start_id - The `id` of the starting message
     * @param {Number} number - The number of messages to be fetched
     * @param {String} url - The `url` where to send the request
     */
    function handle_loaded_messages(direction, messages, new_data) {
        var message;
        var $message_box = $("#message_box");
        if (direction == 'backward') {
            $message_box.data("firstMessageId", new_data);
            messages.forEach(function(message) {
                message = new Message(message.type,
                                      message.author,
                                      message.message,
                                      message.date,
                                      message.file_name,
                                      message.file_url);
                $message_box.prepend(message.create_dom_element());
            });
        } else {
            $message_box.data("lastMessageId", new_data);
            messages.forEach(function(message) {
                message = new Message(message.type,
                                      message.author,
                                      message.message,
                                      message.date,
                                      message.file_name,
                                      message.file_url);
                $message_box.append(message.create_dom_element());
            });
        }
    }

    /**
     * Returns a list of chat messages in JSON format
     * @function
     * @param {String} direction - The direction of fetching. It can be either `backward` or `forward`
     * @param {Number} start_id - The `id` of the starting message
     * @param {Number} number - The number of messages to be fetched
     * @param {String} url - The `url` where to send the request
     * @param {handle_loaded_messages} callback - The callback that handles the response.
     * @returns {JSON}
     */
    function load_messages(direction, start_id, number, url, callback) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            url: url,
            type: 'POST',
            data: {'direction': direction,
                   'start_id': start_id,
                   'number': number },
            cache: false,
            dataType: 'JSON',
            success: function(response) {
                callback(direction, response.messages, response.new_data);
            },
            error: function(data) {

            }
        });
    }


    function send_message(form) {
        var $form = $(form);
        var data = new FormData($('form').get(0));
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                sync_messages();
                $('#chat_form #id_message').val('');
            },
            error: function(data) {
                alert('Error submitting');
            }
        });
        
        return false;
    }

    function sync_messages_cycle() {
        sync_messages();
        setTimeout(function(){
            sync_messages_cycle();
        }, 2000);
    }

    function scroll_to_bottom(element) {
            var $element = $(element);
            var height = $element[0].scrollHeight;
            $element.animate({ scrollTop: height}, 1000);
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    sync_messages_cycle();
});