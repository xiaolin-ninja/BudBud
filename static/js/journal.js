// autocomplete
$( function() {
    $( "#findStrain" ).autocomplete({
      source: {{ auto_strains | tojson }},
      minLength: 2
    });
    console.log('autocomplete working')
  } );

