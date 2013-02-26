places = [{name: '新竹市立體育場',              url: 'http://g.co/maps/xk525'},
          {name: '新竹巨城購物中心7樓溜冰場旁', url: 'http://goo.gl/maps/0AmZO'}]

old_round = ''

initialize = ->
  for p in places
    $('select#place').prepend("<option>#{p.name}</option>")
    $('input#place_url').val(p.url)
  old_round = $('#round').val()
  $('#round').closest('.controls').find('span').hide()
  $('#datepicker').closest('.controls').find('span').hide()

bind_listeners = ->
  $('select#place').change ->
    for p in places
      if $('select#place').val() == p.name
        $('input#place_url').val(p.url)
        break

  $('#submit').click ->
    flag = true

    if $('#round').val() == old_round
      $('#round').closest('.controls').find('span').show()
      $('#round').closest('.control-group').addClass('error')
      flag = false

    if $('#datepicker').val() == ''
      $('#datepicker').closest('.controls').find('span').show()
      $('#datepicker').closest('.control-group').addClass('error')
      flag = false

    $('#round').on 'keyup', ->
      $('#round').closest('.controls').find('span').hide()
      $('#round').closest('.control-group').removeClass('error')

    $('#datepicker').on 'keyup change', ->
      $('#datepicker').closest('.controls').find('span').hide()
      $('#datepicker').closest('.control-group').removeClass('error')

    if flag
      $('form').submit()

$ ->
  initialize()
  bind_listeners()
  
