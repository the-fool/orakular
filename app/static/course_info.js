$(document).ready(function() {
    $('tr').click(function() {
	var id=$(this).data('id');
	var name=$(this).children().eq(1).text();
	console.log(name);
	$('#student_info').data('id', id);
	$('#student_info .modal-title').text(name);
	$('#student_info').modal('show');
	$('#student_info .modal-body').load('/ajax/student_modal?sid='+id);
    });
    
});
