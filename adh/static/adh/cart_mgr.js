


function ScoAdhCartManager(rootUrl, debug) {
    // ----- on fait un genre de singleton/mono instance par rootUrl
    if (ScoAdhCartManager.prototype._instances) {
        if (debug) console.log(`ScoAdhCartManager init - proto inst exists : ${ScoAdhCartManager.prototype._instances}`);
        insts=ScoAdhCartManager.prototype._instances;
    } else {
        if (debug) console.log(`ScoAdhCartManager init - proto inst does NOT exist`);
        insts={}
        ScoAdhCartManager.prototype._instances=insts;
    }
    if (insts[rootUrl]) {
        if (debug) console.log(`ScoAdhCartManager init - proto inst exists for rootUrl ${rootUrl}: ${insts[rootUrl]}`);
        // -- ici on bypasse le constructeur si le "singleton" existe déjà
        return insts[rootUrl];
    } else {
        if (debug) console.log(`ScoAdhCartManager init - proto inst does NOT exist for rootUrl ${rootUrl}`);    
        insts[rootUrl]=this;
    }

    // -- c'est parti pour l'init !

    // Params
    this.debug=debug;
    this.rootUrl=rootUrl;
    // actual cart
    this.scoAdhCart={};
}


// Helpers with constants
ScoAdhCartManager.prototype.getCartStorageKey = function () {
    return this.rootUrl+"--++--//cart//";
}
ScoAdhCartManager.prototype.getCartDiv = function () {
    return document.getElementById("adh_cart_display");
}
ScoAdhCartManager.prototype.getCartSummaryDiv = function () {
    return document.getElementById("adh_cart_summary");
}


// ==================================================
// STORAGE FUNCTIONS

ScoAdhCartManager.prototype.clearAdhCart = function() {
    if (this.debug)  console.log("clearAdhCart - start ");
    this.scoAdhCart={};
    if (this.debug) console.log("clearAdhCart - persist ");
    this.persistAdhCartToStorage();
    if (this.debug) console.log("clearAdhCart - done ");
}

ScoAdhCartManager.prototype.persistAdhCartToStorage = function () {
    if (this.debug) console.log("persistAdhCartToStorage - start ");
    localStorage.setItem(this.getCartStorageKey(), JSON.stringify(this.scoAdhCart));
    if (this.debug) console.log("persistAdhCartToStorage - done ");
}

ScoAdhCartManager.prototype.loadAdhCartFromStorage = function() {
    if (this.debug) console.log("loadAdhCartFromStorage - start ");
    let data=localStorage.getItem(this.getCartStorageKey());
    if (data) {
        this.scoAdhCart = JSON.parse(data);
    } else {
        this.scoAdhCart = {};
        this.persistAdhCartToStorage();
    }
    if (this.debug) console.log("loadAdhCartFromStorage - done ");
}

ScoAdhCartManager.prototype.getCartContentSummary = function () {
    let adh_count=0;
    let adh_sum=0
    for (var key in this.scoAdhCart){
        if (this.debug) console.log("getCartContentSummary ", key, this.scoAdhCart[key] );
        let prod=this.scoAdhCart[key]
        adh_count+=prod.qty
        adh_sum+=(prod.price*prod.qty)
        if (this.debug) console.log("getCartContentSummary - count=", adh_count, " sum=", adh_sum )
    }
    return [adh_count, adh_sum]
}


// ==================================================
// DISPLAY FUNCTIONS 

ScoAdhCartManager.prototype.emptyAndHideCart = function () {
    if (this.debug) console.log("emptyAndHideCart - start");
    this.clearAdhCart();
    this.updateCartBanner();
    this.clearCartDisplay();
    if (this.debug) console.log("emptyAndHideCart - done");
}

ScoAdhCartManager.prototype.cartIsDiplayed= function ()  {
    let myNode = this.getCartDiv();
    if (!myNode)
        return false;
    return myNode.lastElementChild;
}

ScoAdhCartManager.prototype.clearCartDisplay = function () {
    let myNode = this.getCartDiv();
    if (!myNode) return;
    while (myNode.lastElementChild) {
        myNode.removeChild(myNode.lastElementChild);
    }
    myNode.style.display="none";
}

ScoAdhCartManager.prototype.toggleCartDisplay = function () {
    if (this.debug) console.log("toggleCartDisplay")
    if (this.cartIsDiplayed()) {
        this.clearCartDisplay();
    } else {
        this.showOrUpdateCartDisplay();
    }
}

ScoAdhCartManager.prototype.showOrUpdateCartDisplay = function() {
    let mgr=this;
    this.clearCartDisplay();
    let cart_div=this.getCartDiv();
    if (!cart_div){
        cart_div=document.createElement("div");
        cart_div.id="adh_cart_display";
        cart_div.className="my_adh_cart_display";
        cart_div.style.zIndex=100000;
        cart_div.style.display="none";
        cart_div.onclick=function(event){return mgr.toggleCartDisplay(event);};
        document.body.appendChild(cart_div);
    }

    let span =  document.createElement('span');
    span.className = "my_adh_cart_title";
    span.textContent="Mon panier";
    cart_div.append(span);

    let table =  document.createElement('table');
    table.border="1px";
    table.cellSpacing="0px";
    table.cellPadding="5px";
    table.className = "my_adh_cart_table";

    let thead =  document.createElement('thead');

    let head_tr = document.createElement('tr');

    let title_th = document.createElement("td");
    title_th.textContent="ACTIVITE";
    head_tr.appendChild(title_th);

    let price_th = document.createElement("td");
    price_th.textContent="PRIX";
    head_tr.appendChild(price_th);

    let qty_th = document.createElement("td");
    qty_th.textContent="QTÉ";
    head_tr.appendChild(qty_th);

    let actions_th = document.createElement("td");
    actions_th.textContent="ACTIONS";
    head_tr.appendChild(actions_th);

    thead.appendChild(head_tr);

    table.appendChild(thead);

    let tbody=document.createElement('tbody');

    this.loadAdhCartFromStorage();
    if (Object.keys(this.scoAdhCart).length==0) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan=4;
        td.textContent="AUCUNE ACTIVITE DANS LE PANIER";
        tr.appendChild(td);
        tbody.appendChild(tr);
    } else {
        for (let id in this.scoAdhCart) {
            let item = this.scoAdhCart[id];
            let tr = document.createElement('tr');

            let title_td = document.createElement('td');
            title_td.innerHTML = this.spaceToNbsp(item.title);
            title_td.align="left";
            tr.appendChild(title_td);

            let price_td = document.createElement("td");
            price_td.innerHTML = item.price + "&nbsp;€";
            price_td.align="center";
            tr.appendChild(price_td);

            let qty_td = document.createElement("td");
            qty_td.textContent = item.qty;
            qty_td.align="right";
            tr.appendChild(qty_td);

            let actions_td = document.createElement("td");
            actions_td.align="center";
            
            let sub_btn=this.buildButton(item, "-", function (event) { return mgr.subFromCartEvent(event)} );
            actions_td.appendChild(sub_btn);

            let add_btn=this.buildButton(item, "+", function (event) { return mgr.addToCartEvent(event)} );
            actions_td.appendChild(add_btn);

            let rem_btn=this.buildButton(item, "x", function (event) { return mgr.remFromCartEvent(event)} );
            actions_td.appendChild(rem_btn);

            tr.appendChild(actions_td);

            tbody.appendChild(tr);
        }
        
        let total_tr = document.createElement('tr');
        let title_total_td = document.createElement("td");
        title_total_td.colSpan=2;
        title_total_td.align="right";
        title_total_td.textContent="PRIX TOTAL";
        total_tr.appendChild(title_total_td);
        let price_total_td=document.createElement("td");
        price_total_td.align="right";
        price_total_td.innerHTML=this.getCartContentSummary()[1]+"&nbsp;€";
        total_tr.appendChild(price_total_td);
        let actions_total_td=document.createElement("td");
        actions_total_td.align="center";
        let clr_btn=document.createElement("button");
        clr_btn.textContent="VIDER";
        clr_btn.addEventListener("click",  function (event) { return mgr.emptyCartEvent(event)} );
        actions_total_td.appendChild(clr_btn);
        total_tr.appendChild(actions_total_td);

        tbody.appendChild(total_tr);
    }
    table.appendChild(tbody);

    cart_div.appendChild(table);

    /*
    let hide_cart=document.createElement("a");
    hide_cart.href="javascript:clearCartDisplay()";
    hide_cart.text="MASQUER LE PANIER";
    cart_div.appendChild(hide_cart);
    */

    cart_div.style.display="block";
}

ScoAdhCartManager.prototype.updateCartBanner = function () {
    let mgr=this;
    let adh_summary=this.getCartContentSummary();
    let adh_cart_summary=this.getCartSummaryDiv();
    let adh_cart_displayed = this.cartIsDiplayed()
    if (adh_cart_summary) {
        while (adh_cart_summary.lastElementChild) {
            adh_cart_summary.removeChild(adh_cart_summary.lastElementChild);
        }
        ahref=document.createElement("a");
        ahref.href='#';
        ahref.onclick= function (event) { return mgr.toggleCartDisplay(event)};
        ahref.innerHTML =`
            <span class='my_adh_cart_icon'></span>
            ${adh_summary[1]}&nbsp;€
            `;
        adh_cart_summary.appendChild(ahref);
        if (adh_summary[0]>0) {
            adh_cart_summary.style.display="block";
        } else {
            adh_cart_summary.style.display="none";
        }
    }
    if (adh_cart_displayed) 
        this.showOrUpdateCartDisplay();
}

ScoAdhCartManager.prototype.buildButton = function(item, text, func) {
    let btn=document.createElement("button");
    btn.textContent=text;
    btn.dataset.price=item.price;
    btn.dataset.title=item.title;
    btn.dataset.id=item.id;
    btn.onclick=func;
    return btn;
}


// ==================================================
// EVENTS

ScoAdhCartManager.prototype.wireEvents = function () {
    let btns = document.querySelectorAll(".adh_products button");
    let mgr=this;
    console.log("wireEvents - found : ", btns.length);
    for (let i = 0; i < btns.length; i++) {
        let btn = btns[i];
        console.log("adding event on btn ", i+1);
        btn.addEventListener("click", function (event) { return mgr.addToCartEvent(event)});
    };
}

ScoAdhCartManager.prototype.addToCartEvent = function(event) {
    console.log("addToCartEvent - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    console.log("addToCartEvent called with dataset :  id="+id+" title='"+title+"' price="+price  +" / this.scoAdhCart="+this.scoAdhCart);
    if (id in this.scoAdhCart) {
        console.log("addToCartEvent - found existing product -> increment qty");
        this.scoAdhCart[id].qty++;
        //Also update title and price, may be they did change
        this.scoAdhCart[id].title=title
        this.scoAdhCart[id].price=price
    } else {
        console.log("addToCartEvent - new product -> add with qty=1");
        let cartItem = {
            id: id,
            title: title,
            price: price,
            qty: 1
        };
        this.scoAdhCart[id] = cartItem
    }
    if (this.debug) console.log("addToCartEvent - persist ");
    this.persistAdhCartToStorage()
    if (this.debug) console.log("addToCartEvent - updateCartBanner ");
    this.updateCartBanner();
    if (this.debug) console.log("addToCartEvent - stop propagation ");
    event.stopImmediatePropagation();
    if (this.debug) console.log("addToCartEvent - done ");
}

ScoAdhCartManager.prototype.subFromCartEvent = function(event) {
    if (this.debug) console.log("subFromCartEvent - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    if (this.debug) console.log("subFromCartEvent called with dataset :  id="+id+" title='"+title+"' price="+price  +" / this.scoAdhCart="+this.scoAdhCart);
    if (id in this.scoAdhCart) {
        console.log("subFromCartEvent - found existing product -> decrement qty if >0");
        if (this.scoAdhCart[id].qty>0) {
            this.scoAdhCart[id].qty--;
            this.persistAdhCartToStorage()
            this.updateCartBanner();
        } 
    } else {
        // ignore the substraction on non existent id
        if (this.debug) console.log("subFromCartEvent - cannot find entry ", id, "title ", title);
    }
    if (this.debug) console.log("subFromCartEvent - stop propagation ");
    event.stopImmediatePropagation()
}

ScoAdhCartManager.prototype.remFromCartEvent = function (event) {
    if (this.debug) console.log("remFromCartEvent - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    if (this.debug) console.log("remFromCartEvent called with dataset :  id="+id+" title='"+title+"' price="+price  +" / this.scoAdhCart="+this.scoAdhCart);
    if (id in this.scoAdhCart) {
        if (this.debug) console.log("remFromCartEvent - found existing product -> remove from cart");
        delete this.scoAdhCart[id];
        this.persistAdhCartToStorage()
        this.updateCartBanner();
    } else {
        // ignore the removal on non existent id
        if (this.debug) console.log("remFromCartEvent - cannot find entry ", id, "title ", title);
    }
    console.log("remFromCartEvent - stop propagation ");
    event.stopImmediatePropagation()
}

ScoAdhCartManager.prototype.emptyCartEvent = function (event) {
    if (this.debug) console.log("emptyCartEvent - start");
    this.emptyAndHideCart();
    console.log("emptyCartEvent - stop propagation ");
    event.stopImmediatePropagation();
    if (this.debug) console.log("emptyCartEvent - done");
}


// ==================================================
// FORMAT UTILS

ScoAdhCartManager.prototype.spaceToNbsp=function(text) {
    if (this.debug)  console.log("spaceToNbsp - text="+text);
    if (text) {
        if (this.debug) console.log(`spaceToNbsp - return ${text.replace(/ /g, "&nbsp;")}`);
        return text.replace(/ /g, "&nbsp;");
    }
    return "";
}



// ==================================================
// INIT 

ScoAdhCartManager.prototype.initOnDocReady = function () {
    if (this.debug)  console.log("initOnDocReady - start ");
    this.loadAdhCartFromStorage();
    if (this.debug) console.log("initOnDocReady - updateCartBanner ");
    this.updateCartBanner();
    if (this.debug) console.log("initOnDocReady - wire buttons ");
    this.wireEvents();
    if (this.debug) console.log("initOnDocReady - done ");
}







