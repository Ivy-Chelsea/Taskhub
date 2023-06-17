// Close the flash messages when the close button is clicked
var closeButtons = document.getElementsByClassName('flash-message');
for (var i = 0; i < closeButtons.length; i++) {
  closeButtons[i].addEventListener('click', function() {
    this.style.display = 'none';
  });
}

// Automatically hide the flash messages after 5 seconds
var flashMessages = document.getElementsByClassName('flash-messages')[0];
setTimeout(function() {
  flashMessages.style.display = 'none';
}, 5000);