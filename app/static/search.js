$(document).ready(function () {
    $('thead').each(function() {
	$(this).append("<tr class='warning no-result'><td colspan='99'><i class='fa fa-warning'></i> No result</td></tr>"     );
    });
    var default_table = "student";
    $('#table-'+default_table).bootstrapTable('refresh', {url: "/api/"+default_table});
    
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
	var target = $(e.target).attr("href");
	target = target.slice(1);
	$('#table-'+target).bootstrapTable('refresh', {url: "/api/"+target});
	$('.search').val('');
	$('.no-result').hide();
    });

    $(".search").each( function() {
	$(this).keyup(function () {
	    var table = ".results."+$(this).data('id');
	    var searchTerm = $(this).val();
	    var listItem = $(table +' tbody').children('tr');
	    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
	    
	    $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
		return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
	    }});
	    
	    $(table + " tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','false');
	    });
	    
	    $(table + " tbody tr:containsi('" + searchSplit + "')").each(function(e){
		$(this).attr('visible','true');
	    });
	    
	    var jobCount = $(table +' tbody tr[visible="true"]').length;
	    $('.counter').text(jobCount + ' item');
	    
	    if(jobCount == '0') {$('.no-result').show();}
	    else {$('.no-result').hide();}
	});
    });
    
});

function levelSorter(a, b) {
    var levels = { "Freshman":0, "Sophomore":1, "Junior":2, "Senior":3 };
    
    if (levels[a] > levels[b]) return 1;
    if (levels[a] < levels[b]) return -1;
    return 0;
}

function integerFormat(value) {
    return Math.trunc(value);
}
