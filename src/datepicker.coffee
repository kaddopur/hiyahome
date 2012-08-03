places = [{name: '新竹市立體育場',              url: 'http://g.co/maps/xk525'},
          {name: '新竹巨城購物中心7樓溜冰場旁', url: 'http://goo.gl/maps/0AmZO'}]

old_round = ''

initialize = ->
  $('#datepicker').datepicker()
  for p in places
    $('select#place').prepend("<option>#{p.name}</option>")
    $('input#place_url').val(p.url)
  old_round = $('#round').val()
  $('#round ~ span').hide()
  $('#datepicker ~ span').hide()

bind_listeners = ->
  $('select#place').change ->
    for p in places
      if $('select#place').val() == p.name
        $('input#place_url').val(p.url)
        break

  $('#submit').click ->
    flag = true

    if $('#round').val() == old_round
      $('#round ~ span').show()
      $('#round ~ span').parent().parent().addClass('error')
      flag = false

    if $('#datepicker').val() == ''
      $('#datepicker ~ span').show()
      $('#datepicker ~ span').parent().parent().addClass('error')
      flag = false

    $('#round').change ->
      $('#round ~ span').hide()
      $('#round ~ span').parent().parent().removeClass('error')

    $('#datepicker').change ->
      $('#datepicker ~ span').hide()
      $('#datepicker ~ span').parent().parent().removeClass('error')

    if flag
      $('form').submit()

$ ->
  initialize()
  bind_listeners()
  
