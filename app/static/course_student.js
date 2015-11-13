function submitreg() {
    $('#register-form').submit();
}

$(document).ready(function() {
    $('.button-reg').click(function() {
	var id=$(this).data('id');
	$('#student-modal').data('id', id);
	$('#student-modal .modal-title').text("Register for " + id + " (action cannot be undone)");
	$('#cid').val(id);
	$('#student-modal').modal('show');
    });
});
