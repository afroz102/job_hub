$(document).ready(function(){
  $('.datatable-select-inputs').DataTable({
      dom: 'Bfrtip',
      columnDefs: [
            {
                targets: 1,
                className: 'noVis'
            }
      ],
      order: [
        [0, 'desc']
      ],
      buttons: [
            {
                extend: 'colvis',
                text: 'Visible Columns',
                columns: ':not(.noVis)',
                className: 'btn btn-success btn-sm',
                init: function(api, node, config) {
                   $(node).removeClass('dt-button')
                }
            }
      ],
      initComplete: function() {
          this.api().columns([0, 2,]).every(function() {
              console.log(this)
              var column = this;
              var select = $('<select class="form-control custom-select"><option value="">All</option></select>')
                  .appendTo($(column.footer()).empty())
                  .on('change', function() {
                      var val = $.fn.dataTable.util.escapeRegex(
                          $(this).val()
                      );

                      column
                          .search(val ? '^' + val + '$' : '', true, false)
                          .draw();
                  });

              column.data().unique().sort().each(function(d, j) {
                  select.append('<option value="' + d + '">' + d + '</option>');
              });
          });
      }
  });
})
