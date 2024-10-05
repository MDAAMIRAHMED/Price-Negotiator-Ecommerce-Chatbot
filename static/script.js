$(document).ready(function() {
    $("#chatbotToggle").click(function() {
        $("#chatbox").toggle(); // Toggle the chatbox visibility
    });

    $("#send").click(function() {
        let user_input = $("#user_input").val();
        if (user_input.trim() !== "") {
            $("#responses").append(`<div class="user-message"><strong>👤:</strong> ${user_input}</div>`);
            $.post("/chat", { user_input: user_input }, function(data) {
                $("#responses").append(`<div class="chatbot-message"><strong>🤖:</strong> ${data.response}</div>`);
                $("#user_input").val(""); // Clear input field
                $('#responses').scrollTop($('#responses')[0].scrollHeight); // Scroll to bottom
            });
        }
    });

    // Allow pressing Enter to send message
    $("#user_input").keypress(function(e) {
        if (e.which == 13) {
            $("#send").click();
        }
    });
});