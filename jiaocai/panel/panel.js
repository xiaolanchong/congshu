/*
How to use:

1) Create an element
<div id="toggle-panel">
  <label><input type="checkbox" id="chk-source"> Source</label>
  <label><input type="checkbox" id="chk-translation"> Translation</label>
</div>

2) Add links:
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
	<script src="..../panel.js"></script>
	<link href="..../panel.css" rel="stylesheet">

*/

$(function(){
	
 // $(document).ready(function () {
	  const KEY_SOURCE = 'showSource';
	  const KEY_TRANSLATION = 'showTranslation';

	  // Load and apply saved states
	  const savedSource = localStorage.getItem(KEY_SOURCE);
	  const showSource = savedSource === null ? true : JSON.parse(savedSource);
	  $('#chk-source').prop('checked', showSource);

	  const savedTranslation = localStorage.getItem(KEY_TRANSLATION);
	  const showTranslation = savedTranslation === null ? true : JSON.parse(savedTranslation);
	  $('#chk-translation').prop('checked', showTranslation);

	  // Function to update visibility
	  function updateVisibility(){
		$('.source').toggleClass('hidden', !$('#chk-source').is(':checked'));
		$('.translation').toggleClass('hidden', !$('#chk-translation').is(':checked'));
	  }

	  // Initial visibility
	  updateVisibility();

	  // On toggle, update and store
	  $('#chk-source').on('change', function(){
		localStorage.setItem(KEY_SOURCE, $(this).is(':checked'));
		updateVisibility();
	  });
	  $('#chk-translation').on('change', function(){
		localStorage.setItem(KEY_TRANSLATION, $(this).is(':checked'));
		updateVisibility();
	  });
 // });
});