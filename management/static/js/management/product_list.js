function isTableRowMatched(tableRow, queryProduct, queryNStock) {
  if (queryNStock === '') {
    queryNStock = Infinity
  } else {
    queryNStock = parseInt(queryNStock)
  };

  let isProductMatch = tableRow[0].querySelector('.col-complete-name').innerText.split(',')[0].toLowerCase().indexOf(queryProduct) > -1
  let isNStockMatch = parseInt(tableRow[0].querySelector('.col-stock').innerText) < queryNStock
  return isProductMatch && isNStockMatch
}

$(document).ready(function() {
  let queryProduct = ''
  let queryNStock = ''
  $('#search-product').val(queryProduct)
  $('#stock-less-than').val(queryNStock)

  $('#search-product').on('keyup', function() {
    queryProduct = $(this).val().toLowerCase();
    $('#table-product-body tr').filter(function() {
      $(this).toggle(isTableRowMatched($(this), queryProduct, queryNStock))
    });
  });

  $('#stock-less-than').on('keyup', function() {
    queryNStock = $(this).val()
    $('#table-product-body tr').filter(function() {
      $(this).toggle(isTableRowMatched($(this), queryProduct, queryNStock))
    });
  });
})