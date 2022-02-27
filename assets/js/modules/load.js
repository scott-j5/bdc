export const LOAD = {
    request : null,
    loadToElement: async function(element, url){
        var loader = document.createElement("div");
        loader.classList.add("loader");
        element.append(loader);
        element.classList.add('loading');
        
        var response = null;
        try{
            response = await this._load(url, 'text/html');
            LOAD.updateContent(response, element);
        }catch{
            LOAD.showError(response, element);
        }
        element.classList.remove('loading');
    },
    loadJson: async function(url){
        return json.parse(await this._load(url, 'application/json', false));
    },
    _load(url, contentType, data=false){
        return new Promise((resolve, reject) => {
            //Ajax function to get files
            const xhr = new XMLHttpRequest();
            
            if (data){
                xhr.open('POST', url, true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                xhr.send(data); 
            }else{
                xhr.open('GET', url, true);
                xhr.setRequestHeader('Content-Type', contentType);
                xhr.send(null); 
            };

            xhr.onload = function(){
                if(xhr.status == 200){
                    if (contentType = 'application/JSON'){
                        resolve(xhr.responseText);
                    }else{
                        resolve(xhr.response);
                    }
                }else{
                    reject(xhr);
                }
            }
        });
    },
    showError: function(xhr, element=false){
        if(element){
            if (xhr.status == 200 ){
                element.innerHTML = xhr.response;
            }else{
                element.innerHTML = '<div class="form-alert form-error"> Error ' + xhr.status + ': ' + xhr.statusText + '</div>';
            }
        }else{
            console.log('Error ' + xhr.status + ': ' + xhr.statusText);
        }
    },
    updateContent: function(response, element){
        element.innerHTML = response;
    }
};