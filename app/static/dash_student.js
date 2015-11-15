$(document).ready(function() {
    $('tr').click(function() {
	var id=$(this).data('id');
	var title=$(this).children('td').eq(1).text();
	console.log(title);
	$('#classInfo').data('id', id);
	$('#classInfo .modal-title').text(id + ": " + title);
	$('#grade_' + id).toggle();
	$('#classInfo').modal('show');
    });
    $('#classInfo').on('hidden.bs.modal', function (e) {
	var id=$(this).data('id');
	$('#grade_' + id).toggle();
    });
});
