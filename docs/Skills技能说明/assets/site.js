(function () {
  const copy_button_list = Array.from(document.querySelectorAll('.copy_button'));
  const nav_link_list = Array.from(document.querySelectorAll('.nav_link'));
  const current_page = document.body.dataset.page || '';

  function copy_text_to_clipboard(text_value) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text_value);
    }

    return new Promise(function (resolve, reject) {
      const helper_textarea = document.createElement('textarea');
      helper_textarea.value = text_value;
      helper_textarea.setAttribute('readonly', 'readonly');
      helper_textarea.style.position = 'fixed';
      helper_textarea.style.left = '-9999px';
      document.body.appendChild(helper_textarea);
      helper_textarea.select();

      try {
        document.execCommand('copy');
        document.body.removeChild(helper_textarea);
        resolve();
      } catch (error) {
        document.body.removeChild(helper_textarea);
        reject(error);
      }
    });
  }

  function flash_button_state(button_node, is_success) {
    const original_label = button_node.dataset.originalLabel || button_node.textContent;
    button_node.dataset.originalLabel = original_label;
    button_node.textContent = is_success ? 'Copied' : 'Retry';
    button_node.classList.toggle('is_done', is_success);

    window.setTimeout(function () {
      button_node.textContent = original_label;
      button_node.classList.remove('is_done');
    }, 1200);
  }

  function bind_copy_buttons() {
    copy_button_list.forEach(function (button_node) {
      button_node.addEventListener('click', function () {
        copy_text_to_clipboard(button_node.dataset.copyText || '')
          .then(function () {
            flash_button_state(button_node, true);
          })
          .catch(function () {
            flash_button_state(button_node, false);
          });
      });
    });
  }

  function highlight_active_nav() {
    nav_link_list.forEach(function (link_node) {
      link_node.classList.toggle('is_active', link_node.dataset.navPage === current_page);
    });
  }

  bind_copy_buttons();
  highlight_active_nav();
})();
