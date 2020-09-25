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

function synchronizeIsPreparedAndIsPacked() {
  $('#id_is_packed').on('click', function(){
     if (this.checked == true) {
      $('#id_is_prepared')[0].checked = true
     }
  })
  $('#id_is_prepared').on('click', function(){
     if (this.checked == false) {
      $('#id_is_packed')[0].checked = false
     }
  })
}

function synchronizeAutocompleteFieldText(availableObjects, textInputs) {
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
      textInput.attr('value', label);
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

function ProductFormsetManager(availableProducts, purchaseFormsetClass, formsetManagement, purchaseCRUDHtmlObjects) {
  // PROPERTIES
  this.availableProducts = availableProducts
  this.n = $(purchaseFormsetClass).length

  this.initialN = this.n
  this.purchaseForm = $(purchaseFormsetClass).first()
  this.formsetManagement = $('#management-form')

  this.addPurchaseButton = purchaseCRUDHtmlObjects['addPurchaseButton']
  this.removePurchaseButton = purchaseCRUDHtmlObjects['removePurchaseButton']

  this.addCustomPurchasesModal = purchaseCRUDHtmlObjects['addCustomPurchasesModal']
  this.customProductInput = purchaseCRUDHtmlObjects['customProductInput']
  this.generateCustomProductBtn = purchaseCRUDHtmlObjects['generateCustomProductBtn']
  this.generatedProductsContainer = purchaseCRUDHtmlObjects['generatedProductsContainer']
  this.generatedProductList = purchaseCRUDHtmlObjects['generatedProductList']
  this.addCustomPurchasesButton = purchaseCRUDHtmlObjects['addCustomPurchasesButton']

  // FUNCTIONS
  this.initializeInputField = function(newPurchaseForm, initialData) {
    newPurchaseForm.find('b').first().html(this.n + '.')
    let inputFields = newPurchaseForm.find('input')
    inputFields.each((k) => {
      inputFields[k].id = inputFields[k].id.replace(0, this.n-1)
      inputFields[k].name = inputFields[k].id.replace('id_', '')
      if (!initialData) {inputFields[k].value = ''}
      else {
        if (inputFields[k].className.search('has-autocomplete') != -1) {
          if (inputFields[k].id == '') {inputFields[k].value = initialData['label']}
          else {inputFields[k].value = initialData['value']}
        } else if (inputFields[k].id.search('amount') != -1) {
          inputFields[k].value = initialData['amount']
        } else {
          inputFields[k].value = ''
        }
      }
    })
    let labels = newPurchaseForm.find('label')
    labels.each((k) => {
      labels[k].setAttribute('for', labels[k].getAttribute('for').replace(0, this.n-1))
    })
  }

  this.addPurchase = function(initialData) {
    this.n++
    let newPurchaseForm = this.purchaseForm.clone().appendTo(this.purchaseForm.parent())
    this.initializeInputField(newPurchaseForm, initialData)
    this.formsetManagement.find('input').first().val(this.n)
    productTextInputs = $('.product-autocompleter')
    addAutocompleter(this.availableProducts, productTextInputs, true)
    $([document.documentElement, document.body]).animate({
        scrollTop: newPurchaseForm.offset().top
    }, 300);
  }

  this.parseCustomProductInput = function(text) {
    let parsedProducts = []
    let products = text.split(';')
    for (let i = 0; i < products.length; i++) {
      let completeProduct = products[i].trim().split(',')
      let product = {}
      for (let j = 0; j < completeProduct.length; j++) {
        if (j == 0) {
          var [productName, ...colorAmount] = completeProduct[j].trim().split(' ')
          colorAmount = {'color': colorAmount[0], 'amount': colorAmount.length > 1 ? colorAmount[1] : 1}
          product['name'] = productName
          product['colorAmount'] = [colorAmount]
        } else {
          let colorAmount = completeProduct[j].trim().split(' ')
          colorAmount = {'color': colorAmount[0], 'amount': colorAmount.length > 1 ? colorAmount[1] : 1}
          product['colorAmount'].push(colorAmount)
        }
      }
      parsedProducts.push(product)
    }
    return parsedProducts
  }

  this.findProducts = function(parsedProducts) {
    let foundProducts = []
    console.log(parsedProducts)
    for (let i = 0; i < this.availableProducts.length; i++) {
      if (parsedProducts.length == 0) { break }
      let availableProduct = this.availableProducts[i]
      for (let j = 0; j < parsedProducts.length; j ++) {
        let parsedProduct = parsedProducts[j]
        if (parsedProduct['name'].toLowerCase() == availableProduct['name']) {
  //        console.log('product name, color: ' + availableProduct['name'] + ', ' + availableProduct['color'])
  //        console.log('parsed name: ' + parsedProduct['name'])
          for (let k = 0; k < parsedProduct['colorAmount'].length; k ++) {
  //          console.log('parsed color: ' + parsedProduct['colorAmount'][k]['color'])
            if (parsedProduct['colorAmount'][k]['color'].toLowerCase() == availableProduct['color']) {
              temp = {...availableProduct}
              temp['amount'] = parsedProduct['colorAmount'][k]['amount']
              delete temp['name']
              delete temp['color']
              foundProducts.push(temp)
            }
          }
        }
      }
    }
    return foundProducts
  }

  this.addRemoveAddPurchaseHandler = function() {
    this.addPurchaseButton.on('click', (e) => {
      e.preventDefault()
      this.addPurchase()
    })
    this.removePurchaseButton.on('click', (e) => {
      e.preventDefault()
      if (this.n > this.initialN) {
        this.n--
        let lastPurchaseForm = $(purchaseFormsetClass).last()
        lastPurchaseForm.remove()
        this.formsetManagement.find('input').first().val(this.n)
      }
    })
  }

  this.addCustomPurchasesHandler = function() {
    let foundProducts = {}

    this.addCustomPurchasesModal.on('shown.bs.modal', () => {
      this.customProductInput.focus();
    })
    this.generateCustomProductBtn.on('click', () => {
      this.generatedProductsContainer.attr('class', this.generatedProductsContainer.attr('class').replace('d-none', ''))
      this.generatedProductList.empty()
      let parsedProducts = this.parseCustomProductInput(this.customProductInput.val())
      foundProducts = this.findProducts(parsedProducts, this.availableProducts)
      foundProducts.map((product, i) => {
        this.generatedProductList.append('<li>' + product['label'] + ' = ' + product['amount'] + '</li>')
      })
    })
    this.addCustomPurchasesButton.on('click', () => {
      console.log(foundProducts)
      for (i = 0; i < foundProducts.length; i++) {
        this.addPurchase(foundProducts[i])
      }
    })
  }
}

$(document).ready(function() {
  overrideHelpTextLinksTarget('.helptext-urls')
  synchronizeIsPreparedAndIsPacked()

  const availableCities = JSON.parse($('#available_city').text())
  const availableCustomers = JSON.parse($('#available_customer').text())
  const availableProducts = JSON.parse($('#available_product').text())

// SET AUTOCOMPLETE
  const cityTextInputs = $('.city-autocompleter')
  const customerTextInputs = $('.customer-autocompleter')
  let productTextInputs = $('.product-autocompleter')
  addAutocompleter(availableCustomers, customerTextInputs)
  addAutocompleter(availableCities, cityTextInputs)
  addAutocompleter(availableProducts, productTextInputs)
  synchronizeAutocompleteFieldText(availableCustomers, customerTextInputs)
  synchronizeAutocompleteFieldText(availableCities, cityTextInputs)
  synchronizeAutocompleteFieldText(availableProducts, productTextInputs)

  
  const purchaseFormsetClass = '.purchase-formset'
  const formsetManagement = $('#management-form')
  const purchaseCRUDHtmlObjects = {
    'addPurchaseButton': $('#add-purchase-button'),
    'removePurchaseButton': $('#remove-purchase-button'),
    'addCustomPurchasesModal': $('#addCustomPurchasesModal'),
    'customProductInput': $('#custom-product-input'),
    'generateCustomProductBtn': $('#generate-custom-product'),
    'generatedProductsContainer': $('#generated-product-container'),
    'generatedProductList': $('#generated-product-list'),
    'addCustomPurchasesButton': $('#add-custom-purchases-btn'),
  }
  pfManager = new ProductFormsetManager(availableProducts, purchaseFormsetClass, formsetManagement, purchaseCRUDHtmlObjects)
  pfManager.addRemoveAddPurchaseHandler()
  pfManager.addCustomPurchasesHandler()
})