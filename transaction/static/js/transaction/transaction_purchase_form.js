function overrideHelpTextLinksTarget(class_name) {
  $(class_name).each((idx, helptextUrl) => {
    windows = {}
    helptextUrl = $(helptextUrl)
    helptextUrl.click((e) => {
      e.preventDefault()
      url = helptextUrl.attr('href')
      windows[helptextUrl.attr('id')] = window.open(url, '_blank', 'resizable=0,menubar=0,width=500,height=600')
    })
  })
}

function adjustAutocompleteFieldText(availableObjects, textInputs) {
  textInputs.each((idx, textInput) => {
    textInput = $(textInput)
    let label = ''
    const value = parseInt(textInput.val())
    if (value) {
      for (let i = 0; i < availableObjects.length; i++) {
        if (availableObjects[i]['value'] == value) {
          label = availableObjects[i]['label']
          break
        }
      };
      textInput.val(label);
    }
  })
}

function addAutocompleter(availableObjects, textInputs) {
  textInputs.each((idx, textInput) => {
    textInput = $(textInput)
    textInput.autocomplete({
      minLength: 1,
      source: availableObjects,
      focus: function( event, ui ) {
        return false;
      },
      select: function( event, ui ) {
        textInput.val(ui.item.label)
        textInput.next().val(ui.item.value)
        return false;
      }
    })
//    .focus(function(){
//        $(this).autocomplete('search', $(this).val());
//    });
  })
}

function initializeInputField(newPurchaseForm, n) {
//  console.log(newPurchaseForm)
  newPurchaseForm.find('b').first().html(n + '.')
  inputFields = newPurchaseForm.find('input')
  inputFields.each((k) => {
    inputFields[k].id = inputFields[k].id.replace(0, n-1)
    inputFields[k].name = inputFields[k].id.replace(0, n-1).replace('id_', '')
    inputFields[k].value = ''
//    console.log(inputFields[k].id)
  })
}

$(document).ready(function() {
  overrideHelpTextLinksTarget('.helptext-urls')

  const availableCities = JSON.parse($('#available_city').text())
  const availableCustomers = JSON.parse($('#available_customer').text())
  const availableProducts = JSON.parse($('#available_product').text())

// SET CITY AUTOCOMPLETE
  const cityTextInputs = $('.city-autocompleter')
  const customerTextInputs = $('.customer-autocompleter')
  let productTextInputs = $('.product-autocompleter')
  addAutocompleter(availableCustomers, customerTextInputs)
  addAutocompleter(availableCities, cityTextInputs)
  addAutocompleter(availableProducts, productTextInputs)
  adjustAutocompleteFieldText(availableCustomers, customerTextInputs)
  adjustAutocompleteFieldText(availableCities, cityTextInputs)
  adjustAutocompleteFieldText(availableProducts, productTextInputs)

// ADD-AND-REMOVE PURCHASE_BUTTON FUNCTIONALITY
  let n = $('.purchase-formset').length
  const initialN = n
  const purchaseForm = $('.purchase-formset').first()
  const formsetManagement = $('#management-form')
  $('#add-purchase-button').on('click', (e) => {
    e.preventDefault()
    n++
    let newPurchaseForm = purchaseForm.clone().appendTo(purchaseForm.parent())
    initializeInputField(newPurchaseForm, n)
    formsetManagement.find('input').first().val(n)
    productTextInputs = $('.product-autocompleter')
    addAutocompleter(availableProducts, productTextInputs, true)
    $([document.documentElement, document.body]).animate({
        scrollTop: newPurchaseForm.offset().top
    }, 300);
  })
  $('#remove-purchase-button').on('click', (e) => {
    e.preventDefault()
    if (n > initialN) {
      n--
      let lastPurchaseForm = $('.purchase-formset').last()
      lastPurchaseForm.remove()
      formsetManagement.find('input').first().val(n)
    }
  })
})