function fixCallbacks(settings) {
    /* Takes a settings object. Converts known callback keys to global
     * window functions. */
    var callback, callbacks = [
        'setup', 'init_instance_callback', 'color_picker_callback',
        'file_picker_callback', 'file_browser_callback'
    ];
    while (callback = callbacks.pop()) {
        if (callback in settings && window[settings[callback]]) {
            settings[callback] = window[settings[callback]];
        }
    }
    settings['images_upload_handler'] = custom_image_upload_handler,
    console.log(settings);
    return settings;
}

function custom_image_upload_handler (blobInfo, success, failure, progress) {
    var xhr, formData;

    xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    xhr.open('POST', '/blogs/blog/default/image/upload/');
    xhr.setRequestHeader('Accept', 'application/json');

    xhr.upload.onprogress = function (e) {
      progress(e.loaded / e.total * 100);
    };
  
    xhr.onload = function() {
      var json;
  
      if (xhr.status === 403) {
        failure('HTTP Error: ' + xhr.status, { remove: true });
        return;
      }
  
      if (xhr.status < 200 || xhr.status >= 300) {
        failure('HTTP Error: ' + xhr.status + '. <br>' + xhr.responseText);
        console.log(xhr)
        return;
      }
  
      json = JSON.parse(xhr.responseText);
  
      if (!json || typeof json.location != 'string') {
        failure('Invalid JSON: ' + xhr.responseText);
        return;
      }
  
      success(json.location);
    };
  
    xhr.onerror = function () {
      failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
    };
  
    formData = new FormData();
    formData.append('image', blobInfo.blob(), blobInfo.filename());
    formData = append_csrf(formData)

    xhr.send(formData);
};


function append_csrf(formData) {
    var csrfToken = getCookie("csrftoken");
    if (!csrfToken) csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    formData.append("csrfmiddlewaretoken", csrfToken);
    return formData;
}


function getCookie(name) {
    if (document.cookie && document.cookie.length) {
        var cookies = document.cookie.split(";").filter(function(cookie) {
            return cookie.indexOf(name + "=") !== -1;
        })[0];
        try {
            return decodeURIComponent(cookies.trim().substring(name.length + 1));
        } catch (e) {
            if (e instanceof TypeError) {
                console.info('No cookie with key "' + name + '". Wrong name?');
                return null;
            }
            throw e;
        }
    }
    return null;
}

if (!tinymce.editors[id]) {
    settings.selector = "#" + id;
    tinymce.init(fixCallbacks(settings));
}
