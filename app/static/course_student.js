$(document).ready(function() {
    $('.button-reg').click(function() {
	var id=$(this).data('id');
	$('#student-modal').data('id', id);
	$('#student-modal .modal-title').text("Register for " + id);
	$('#student-modal').modal('show');
    });
    
});
