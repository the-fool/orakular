$(document).ready(function () {
    var default_table = "student";
    $('#table-'+default_table).bootstrapTable('refresh', {url: "/api/"+default_table});
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	target = target.slice(1);
	$('#table-'+target).bootstrapTable('refresh', {url: "/api/"+target});
    });
});
