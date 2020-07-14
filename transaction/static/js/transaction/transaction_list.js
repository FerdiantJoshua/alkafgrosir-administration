String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

$(document).ready(function() {
  $('.purchase-detail-button').each((key, value) => {
    value.addEventListener('click', () => {
      console.log(value)
      var id = value.parentElement.id.split('_').pop()
      var transactionDate = $('#transaction_date_' + id).text()
      var transactionNumber = $('#transaction_number_' + id).text()
      var transactionCustomer = $('#transaction_customer_' + id).text()
      $('#purchaseDetailModalTitle').text('Transaction #{0} on {1} ({2})'.format(
        transactionNumber, transactionDate, transactionCustomer)
       )
      $('#purchaseDetailModalBody').html(($('#transaction_purchase_' + id).find('.d-none').html()))
    })
  })
})