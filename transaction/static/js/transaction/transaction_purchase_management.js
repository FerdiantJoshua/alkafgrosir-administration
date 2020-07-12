function setTextAutocomplete(availableObjects, textInputIdArray, setHelpText) {
  textInputIdArray.map((id) => {
    $('#' + id).autocomplete({
      minLength: 2,
      source: availableObjects,
      select: function( event, ui ) {
        $('#' + id).val(ui.item.value)
        if (setHelpText) {$('#' + id).next().html(ui.item.label)}
        return false;
      }
    });
  })
}

function initializeInputFieldAndManagementFormset(newPurchaseForm, formsetManagement, n) {
//  console.log(newPurchaseForm)
  newPurchaseForm.find('b').first().html(n + '.')
  newPurchaseForm.find('small').first().html('')
  inputFields = newPurchaseForm.find('input')
  inputFields.each((k) => {
    inputFields[k].id = inputFields[k].id.replace(0, n-1)
    inputFields[k].name = inputFields[k].id.replace(0, n-1)
    inputFields[k].value = ''
//    console.log(inputFields[k].id)
  })
//  console.log(formsetManagement)
  formsetManagement.find('input').first().val(n)
}

$(document).ready(function() {
  const availableProducts = JSON.parse($('#available_product').html().trim())
  const availableCities = JSON.parse($('#available_city').html().trim())
  console.log(availableProducts)
  console.log(availableCities)

  const productTextInputRegex = new RegExp('id_purchase_set-[0-9]+-product', 'g')
  const productTextInputs = $('#purchases').html().match(productTextInputRegex)
  console.log(productTextInputs)
  const cityTextInputs = ['id_city']
  console.log(cityTextInputs)
  setTextAutocomplete(availableProducts, productTextInputs, true)
  setTextAutocomplete(availableCities, cityTextInputs, false)

  var n = 1
  const purchaseForm = $('.purchase-formset')
  const formsetManagement = $('#management-form')

  $('#add-purchase-button').on('mousedown', () => {
    n++
    newPurchaseForm = purchaseForm.clone().appendTo(purchaseForm.parent())
    initializeInputFieldAndManagementFormset(newPurchaseForm, formsetManagement, n)
    setTextAutocomplete(availableProducts, productTextInputs, true)
  })
})