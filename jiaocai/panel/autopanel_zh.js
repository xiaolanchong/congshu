/*
	Creates a popup panel with 2 checkboxes:
	 x ZH&Pinyin x Translation 
*/
const createPanel = () => {
  const html = `
  		<div id="toggle-panel" class="border border-secondary">
		  <label><input type="checkbox" id="chk-source">汉子与拼音</label>
		  <label><input type="checkbox" id="chk-translation">Translation</label>
		</div>`  
  const panel = $(html)
  $(panel).css({
	  position: 'fixed',
	  top: '10px',
	  right: '10px',
	  padding: '8px 12px',
	  'border-radius': '4px',
	  'z-index': '9999',
	  'font-family': 'sans-serif',
	  'font-size': '14px',
  })
  $('label', panel).css({
	'margin-right': '5px',
  })
  $('body').append(panel)
}

const injectStyle = () => {
  $('head').append(`
	<style>
	  .hidden, .hidden > *{
		color: transparent !important;
	}
	</style>
  `)
}

$(function(){
  const KEY_SOURCE = 'showSource';
  const KEY_TRANSLATION = 'showTranslation';

  injectStyle()
  createPanel()
  
  // Load and apply saved states
  const savedSource = localStorage.getItem(KEY_SOURCE);
  const showSource = savedSource === null ? true : JSON.parse(savedSource);
  $('#chk-source').prop('checked', showSource);

  const savedTranslation = localStorage.getItem(KEY_TRANSLATION);
  const showTranslation = savedTranslation === null ? true : JSON.parse(savedTranslation);
  $('#chk-translation').prop('checked', showTranslation);

  // Function to update visibility
  function updateVisibility(){
	$('.chinese, .pinyin').toggleClass('hidden', !$('#chk-source').is(':checked'));
	$('.english').toggleClass('hidden', !$('#chk-translation').is(':checked'));
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
});