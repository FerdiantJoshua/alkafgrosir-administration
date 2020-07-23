String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace('{' + k + '}', arguments[k])
  }
  return a
}

function initializeColumnVisibility(colVisButtonIdPrefix, colTargetClass, columnHideData) {
  for (let i = 0; i < columnHideData.length; i++) {
    id = columnHideData[i]
    const colVisButton = $(colVisButtonIdPrefix + id)
    const colTargets = $(colTargetClass + id)
    colVisButton.removeClass('active')
    colTargets.addClass('d-none')
  }
}

function setColumnVisibilityDropdownMenuItemOnClick(colVisButtons, colTargetClass, columnHideData) {
  colVisButtons.each((idx, colVisButton) => {
    colVisButton = $(colVisButton)
    colVisButton.on('click', (e) => {
      e.preventDefault()
      const target = colVisButton.attr('id').split('-').pop()
      const colTargets = $(colTargetClass + target)
      if (colVisButton.attr('class').split(' ').includes('active')) {
        colVisButton.removeClass('active')
        colTargets.addClass('d-none')
        columnHideData.push(target)
        window.name = JSON.stringify(columnHideData)
      } else {
        colVisButton.addClass('active')
        colTargets.removeClass('d-none')
        columnHideData.pop(target)
        window.name = JSON.stringify(columnHideData)
      }
    })
  })
}

function setPurchaseDetailButtonsOnClick(purchaseDetailButtons) {
  purchaseDetailButtons.each((idx, button) => {
    button = $(button)
    button.click(() => {
      var id = button.parent().attr('id').split('_').pop()
      var transactionDate = $('#transaction_date_' + id).text()
      var transactionNumber = $('#transaction_number_' + id).text()
      var transactionCustomer = $('#transaction_customer_' + id).text()
      $('#purchaseDetailModalTitle').text('Transaction #{0} on {1} ({2})'.format(
        transactionNumber, transactionDate, transactionCustomer)
       )
      $('#purchaseDetailModalBody').html(($('#transaction_purchase_' + id).find('.d-none').html()))
    })
  })
}

$(document).ready(function() {
  let columnHideData = window.name === '' ? [] : JSON.parse(window.name)
  console.log(columnHideData)
  let [colVisButtonClass, colVisButtonIdPrefix] = ['.col-vis-btn', '#col-vis-btn-']
  let colVisButtons = $(colVisButtonClass)
  let colTargetClass = '.col-'

  initializeColumnVisibility(colVisButtonIdPrefix, colTargetClass, columnHideData)
  setColumnVisibilityDropdownMenuItemOnClick(colVisButtons, colTargetClass, columnHideData)

  setPurchaseDetailButtonsOnClick($('.purchase-detail-button'))
})