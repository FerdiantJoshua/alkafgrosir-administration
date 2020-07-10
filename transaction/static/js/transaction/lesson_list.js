$(document).ready(function() {
  $('.book-button').each((key, value) => {
    value.addEventListener('click', () => {
      $('#modal-body').empty()
      $('#lesson_'+value.id).children().clone().appendTo('#modal-body')
      $('#modal-body').children('p').remove()
      $('#id_lesson')[0].value = value.id
    })
  })
})