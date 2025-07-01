
function ScoAdhActivityManager(rootUrl, debug, cartMgr) {
    this.debug=debug;
    this.rootUrl=rootUrl;
    this.cartMgr=cartMgr;
}

ScoAdhActivityManager.prototype.showActivite = function (activite) {
    if (this.debug) console.log("showActivite - start ");
    let manager = this
    $.ajax({
        url: this.rootUrl+'/act/json_activite/'+activite+'/',
        type: "GET",
        contentType: "application/json; charset=utf-8",
        cache: false,
        dataType: "json",		
        xhrFields: { withCredentials: true },	
        success: function (data) { manager.updateActDisplay(data) }
        }
    );
    if (this.debug) console.log("showActivite - done ");
}   

ScoAdhActivityManager.prototype.updateActDisplay = function (data) {
    var text = JSON.stringify(data);
    if (this.debug)  $(".act_debug_panel").text(text);
    let nom_act=this.spaceToNbsp(`Saison ${data.saison.start_year}/${data.saison.start_year+1} `);
    let html_head=`
    <table border="1px" cellspacing="0px" cellpadding="5px">
        <thead>
            <tr>
                <td>${nom_act}</td>
                <td>DATE NAISS.</td>
                <td>PRIX</td>
                <td>ACTION</td>
            </tr>
        </thead>
        <tbody class="adh_products">`;
    let html_body="";
    let variantes=data.variantes;
    for (var v in variantes){
        let variante=variantes[v];
        let vardesc=this.spaceToNbsp(data.nom);
        if (variante.description!="") 
            vardesc+="<br/><i><b>"+variante.description+"</b></i>";
        if (this.debug) console.log("VAR DESC = "+vardesc);
        let pricebyages = variante.pricebyage_set;
        for (var p in pricebyages) {
            let pba=pricebyages[p];
            let body_part=`
            <tr>
                <td>${vardesc}</td>
                <td>${this.getAdhBirthString(pba.min_birth,pba.max_birth)}</td>
                <td align="right">${this.getAdhPriceString(pba.min_price,pba.max_price)}</td>
                <td align="center">
                    <button enabled="${(variante.ouverte && pba.max_price)?true:false}" class="btn btn-primary" 
                    data-id="${pba.id}" data-price="${pba.max_price}" 
                    data-title="${this.adhEscapeString(nom_act)}<br/>${this.adhEscapeString(vardesc)}${this.adhEscapeString(this.spaceToNbsp(this.getAdhTitleBirthString(pba.min_birth,pba.max_birth)))}">AJOUTER</button>
            </tr>`;
            html_body+=body_part;
        }
    }
    let html_tail=`
        </tbody>
    </table>                
    `;

    document.getElementById("adh_products_display").innerHTML=html_head+html_body+html_tail;
    if (this.cartMgr) this.cartMgr.wireEvents();
}

// init function
ScoAdhActivityManager.prototype.adhLoadActivite = function() {
    if (this.debug) console.log("adhLoadActivite - start ");
    let activite=document.getElementById("adh_variante_activite").value;
    if (activite) {
        if (this.debug) console.log("adhLoadActivite - showActivite ");
        this.showActivite(activite);
    }
    if (this.debug) console.log("adhLoadActivite - done ");
}


// Dropdown actvités
ScoAdhActivityManager.prototype.refillDropDown = function() {
    let manager = this
    $.ajax({
        url: this.rootUrl+'/act/json_activites/',
        type: "GET",
        contentType: "application/json; charset=utf-8",
        cache: false,
        dataType: "json",		
        xhrFields: { withCredentials: true },	
        success: function (data) { manager.updateDropDown(data) }
        }
    );
}    
    
ScoAdhActivityManager.prototype.updateDropDown = function(data) {
    let dd=document.getElementById("adh_variante_activite");
    val=dd.value
    while (dd.lastElementChild) {
        dd.removeChild(dd.lastElementChild);
    }
    for (var a in data) {
        act=data[a]
        opt=document.createElement("option")
        opt.value=act.slug
        opt.text=act.nom
        opt.selected=(val==act.slug)
        dd.appendChild(opt)
    }
    this.adhLoadActivite()
}




// ==================================================
// FORMAT UTILS

ScoAdhActivityManager.prototype.adhEscapeString=function (text) {
    if (this.debug)  console.log("escapeString - text="+text);
    if (text) {
        let ret=text.replace(/[\"&'\/<>]/g, 
            function (a) {
                return {
                        '"': '&quot;', '&': '&amp;', "'": '&#39;',
                        '/': '&#47;',  '<': '&lt;',  '>': '&gt;'
                    }[a];
            });
        if (this.debug) console.log(`escapeString - return ${ret}`);
        return ret;
    }
    return "";
}

ScoAdhActivityManager.prototype.formatBirthString= function(birth) {
    var date = new Date(birth);
    var d = date.getDate();
    var m = date.getMonth() + 1; //Month from 0 to 11
    var y = date.getFullYear();
    return `${d <= 9 ? '0' + d : d}/${m<=9 ? '0' + m : m}/${y}`;
}

ScoAdhActivityManager.prototype.getAdhPriceString=function(min_price, max_price) {
    if (!min_price && !max_price) 
        return "INCONNU";
    if (min_price && max_price) {
        if (min_price==max_price)
            return  `${max_price}&nbsp;€`;
        return `entre ${min_price}&nbsp;€ et ${max_price}&nbsp;€`;
    }
    if (min_price)
        return `minimum ${min_price}&nbsp;€`;
    return `maximum ${max_price}&nbsp;€`;
}

ScoAdhActivityManager.prototype.getAdhBirthString=function(min_birth, max_birth) {
    if (!min_birth && !max_birth) 
        return "pas de contrainte";
    if (min_birth && max_birth) 
        return `entre le ${this.formatBirthString(min_birth)} et le ${this.formatBirthString(max_birth)}`;
    if (min_birth)
        return `après le ${this.formatBirthString(min_birth)}`;
    return `avant le ${this.formatBirthString(max_birth)}`;
}

ScoAdhActivityManager.prototype.getAdhTitleBirthString=function(min_birth, max_birth) {
    if (!min_birth && !max_birth) 
        return "";
    if (min_birth && max_birth) 
        return `<br/>Né(e) entre le ${this.formatBirthString(min_birth)} et le ${this.formatBirthString(max_birth)}`;
    if (min_birth)
        return `<br/>Né(e) après le ${this.formatBirthString(min_birth)}`;
    return `<br/>Né(e) avant le ${this.formatBirthString(max_birth)}`;
}

ScoAdhActivityManager.prototype.spaceToNbsp=function(text) {
    if (this.debug)  console.log("spaceToNbsp - text="+text);
    if (text) {
        if (this.debug) console.log(`spaceToNbsp - return ${text.replace(/ /g, "&nbsp;")}`);
        return text.replace(/ /g, "&nbsp;");
    }
    return "";
}


