$(document).ready(function() {
    $('tr').click(function() {
	console.log("clicked:" + $(this).data('id'));
	$('#classInfo .modal-title').text($(this).data('id'));
	$('#classInfo').modal('show');
    });
});
