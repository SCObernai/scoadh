"use strict";

/*
based on https://github.com/hamidhaghdoost/js-shopping-cart/blob/master/js/app.js
*/
$( document ).ready(function() {
    initAdhOnLoad();
    adhLoadActivite();
});

let adh_cart = {};

function initAdhOnLoad() {
    //console.log("initAdhOnLoad - start ");
    if (localStorage.getItem("adh_cart")) {
        //console.log("initAdhOnLoad - loadAdhCartFromStorage ");
        loadAdhCartFromStorage();
    } else {
        //console.log("initAdhOnLoad - initOrClearAdhCart ");
        initOrClearAdhCart();
    }
    //console.log("initAdhOnLoad - updateAdhCartBanner ");
    updateAdhCartBanner();
    //console.log("initAdhOnLoad - wire buttons ");
    wireEvents();
    //console.log("initAdhOnLoad - done ");
}

function wireEvents() {
    let btns = document.querySelectorAll(".adh_products button");
    console.log("wireEvents - found : ", btns.length);
    for (let i = 0; i < btns.length; i++) {
        let btn = btns[i];
        console.log("adding event on btn ", i+1);
        btn.addEventListener("click", addAdhToCart);
    };
}

function initOrClearAdhCart() {
    //console.log("initOrClearAdhCart - start ");
    adh_cart={};
    //console.log("initOrClearAdhCart - persist ");
    persistAdhCartToStorage();
    //console.log("initOrClearAdhCart - done ");
    updateAdhCartBanner();
}

function persistAdhCartToStorage() {
    //console.log("persistAdhCartToStorage - start ");
    localStorage.setItem("adh_cart", JSON.stringify(adh_cart));
    //console.log("persistAdhCartToStorage - done ");
}

function loadAdhCartFromStorage() {
    //console.log("loadAdhCartFromStorage - start ");
    adh_cart = JSON.parse(localStorage.getItem("adh_cart"));
    //console.log("loadAdhCartFromStorage - done ");
}

function addAdhToCart(event) {
    console.log("adhAddToCart - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    console.log("adhAddToCart called with dataset :  id="+id+" title='"+title+"' price="+price  +" / adh_cart="+adh_cart);
    if (id in adh_cart) {
        console.log("adhAddToCart - found existing product -> increment qty");
        adh_cart[id].qty++;
        //Also update title and price, may be they did change
        adh_cart[id].title=title
        adh_cart[id].price=price
    } else {
        console.log("adhAddToCart - new product -> add with qty=1");
        let cartItem = {
            id: id,
            title: title,
            price: price,
            qty: 1
        };
        adh_cart[id] = cartItem
    }
    console.log("adhAddToCart - persist ");
    persistAdhCartToStorage()
    console.log("adhAddToCart - updateAdhCartBanner ");
    updateAdhCartBanner();
    console.log("adhAddToCart - done ");
}

function subAdhFromCart(event) {
    //console.log("subAdhFromCart - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    //console.log("subAdhFromCart called with dataset :  id="+id+" title='"+title+"' price="+price  +" / adh_cart="+adh_cart);
    if (id in adh_cart) {
        console.log("subAdhFromCart - found existing product -> decrement qty if >0");
        if (adh_cart[id].qty>0) {
            adh_cart[id].qty--;
            persistAdhCartToStorage()
            updateAdhCartBanner();
        } 
    } else {
        // ignore the substraction on non existent id
        //console.log("subAdhFromCart - cannot find entry ", id, "title ", title);
    }
}

function remAdhFromCart(event) {
    //console.log("remAdhFromCart - start");
    let price = Number(event.target.dataset.price);
    let title = event.target.dataset.title;
    let id = event.target.dataset.id;
    //console.log("remAdhFromCart called with dataset :  id="+id+" title='"+title+"' price="+price  +" / adh_cart="+adh_cart);
    if (id in adh_cart) {
        //console.log("remAdhFromCart - found existing product -> remove from cart");
        delete adh_cart[id];
        persistAdhCartToStorage()
        updateAdhCartBanner();
    } else {
        // ignore the removal on non existent id
        //console.log("remAdhFromCart - cannot find entry ", id, "title ", title);
    }
}

function getAdhCartContentSummary() {
    let adh_count=0;
    let adh_sum=0
    for (var key in adh_cart){
        //console.log("getAdhCartContentSummary ", key, adh_cart[key] );
        let prod=adh_cart[key]
        adh_count+=prod.qty
        adh_sum+=(prod.price*prod.qty)
        //console.log("getAdhCartContentSummary - count=", adh_count, " sum=", adh_sum )
    }
    return [adh_count, adh_sum]
}

function updateAdhCartBanner() {
    let adh_summary=getAdhCartContentSummary();
    let adh_cart_summary=document.getElementById("adh_cart_summary");
    if (adh_cart_summary) {
        adh_cart_summary.innerHTML =`<a href="javascript:showOrUpdateCartDisplay()">Contenu du panier</a> : ${adh_summary[0]} activités -  ${adh_summary[1]} €`;
        if (adh_summary[0]>0) {
            adh_cart_summary.style.display="block";
        } else {
            adh_cart_summary.style.display="none";
        }
    }
    if (cartIsDiplayed()) 
        showOrUpdateCartDisplay();
}

function cartIsDiplayed() {
    let tbody = document.getElementById("adh_cart_display");
    return tbody.lastElementChild
}

function showOrUpdateCartDisplay() {
    clearCartDisplay();

    let cart_div=document.getElementById("adh_cart_display");

    let table =  document.createElement('table');
    table.border="1px";
    table.cellSpacing="0px";
    table.cellPadding="5px";

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

    loadAdhCartFromStorage();
    if (Object.keys(adh_cart).length==0) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan=4;
        td.textContent="AUCUNE ACTIVITE DANS LE PANIER";
        tr.appendChild(td);
        tbody.appendChild(tr);
    } else {
        for (let id in adh_cart) {
            let item = adh_cart[id];
            let tr = document.createElement('tr');

            let title_td = document.createElement('td');
            title_td.textContent = item.title;
            title_td.align="left";
            tr.appendChild(title_td);

            let price_td = document.createElement("td");
            price_td.textContent = item.price + " €";
            price_td.align="center";
            tr.appendChild(price_td);

            let qty_td = document.createElement("td");
            qty_td.textContent = item.qty;
            qty_td.align="right";
            tr.appendChild(qty_td);

            let actions_td = document.createElement("td");
            actions_td.align="center";
            
            let sub_btn=buildAdhButton(item, "-", subAdhFromCart);
            actions_td.appendChild(sub_btn);

            let add_btn=buildAdhButton(item, "+", addAdhToCart);
            actions_td.appendChild(add_btn);

            let rem_btn=buildAdhButton(item, "x", remAdhFromCart);
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
        price_total_td.textContent=getAdhCartContentSummary()[1]+" €";
        total_tr.appendChild(price_total_td);
        let actions_total_td=document.createElement("td");
        actions_total_td.align="center";
        let clr_btn=document.createElement("button");
        clr_btn.textContent="x";
        clr_btn.onclick=initOrClearAdhCart;
        actions_total_td.appendChild(clr_btn);
        total_tr.appendChild(actions_total_td);

        tbody.appendChild(total_tr);
    }
    table.appendChild(tbody);

    cart_div.appendChild(table);

    let hide_cart=document.createElement("a");
    hide_cart.href="javascript:clearCartDisplay()";
    hide_cart.text="MASQUER LE PANIER";
    cart_div.appendChild(hide_cart);
}

function clearCartDisplay() {
    let myNode = document.getElementById("adh_cart_display");
    while (myNode.lastElementChild) {
        myNode.removeChild(myNode.lastElementChild);
    }
}

function buildAdhButton(item, text, func) {
    let btn=document.createElement("button");
    btn.textContent=text;
    btn.dataset.price=item.price;
    btn.dataset.title=item.title;
    btn.dataset.id=item.id;
    btn.onclick=func;
    return btn;
}
function adhLoadActivite() {
    //console.log("adhLoadActivite - start ");
    let activite=document.getElementById("adh_variante_activite").value;
    //console.log("adhLoadActivite - showActivite ");
    showActivite(activite);
    //console.log("adhLoadActivite - done ");
}

function showActivite(activite) {
    //console.log("showActivite - start ");
    $.getJSON('https://adh.tib.cc/adh/json_activite/'+activite, function(data) {
        //var text = JSON.stringify(data);
        //$(".adh_debug_panel").text(text);
        let nom_act=`${data.nom} - ${data.periode.label}`;
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
        let variantes=data.variante_set;
        for (var v in variantes){
            let variante=variantes[v];
            let pricebyages = variante.pricebyage_set;
            for (var p in pricebyages) {
                let pba=pricebyages[p];
                let body_part=`
                <tr>
                    <td>${variante.description}</td>
                    <td>${getAdhBirthString(pba.min_birth,pba.max_birth)}</td>
                    <td align="right">${getAdhPriceString(pba.min_price,pba.max_price)}</td>
                    <td align="center">
                      <button enabled="${(variante.ouverte && pba.max_price)?true:false}" class="btn btn-primary" 
                        data-id="${pba.id}" data-price="${pba.max_price}" 
                        data-title="${nom_act}&nbsp;-&nbsp;${variante.description}${getAdhTitleBirthString(pba.min_birth,pba.max_birth)}">AJOUTER</button>
                </tr>`;
                html_body+=body_part;
            }
        }
        let html_tail=`
            </tbody>
        </table>                
        `;

        document.getElementById("adh_products_display").innerHTML=html_head+html_body+html_tail;
        wireEvents();
    });
    //console.log("showActivite - done ");
}

function getAdhPriceString(min_price, max_price) {
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

function getAdhBirthString(min_birth, max_birth) {
    if (!min_birth && !max_birth) 
        return "pas de contrainte";
    if (min_birth && max_birth) 
        return `entre le ${formatBirthString(min_birth)} et le ${formatBirthString(max_birth)}`;
    if (min_birth)
        return `après le ${formatBirthString(min_birth)}`;
    return `avant le ${formatBirthString(max_birth)}`;
}

function getAdhTitleBirthString(min_birth, max_birth) {
    if (!min_birth && !max_birth) 
        return "";
    if (min_birth && max_birth) 
        return `- né(e) entre le ${formatBirthString(min_birth)} et le ${formatBirthString(max_birth)}`;
    if (min_birth)
        return `- né(e) après le ${formatBirthString(min_birth)}`;
    return `- né(e) avant le ${formatBirthString(max_birth)}`;
}

function formatBirthString(birth) {
    var date = new Date(birth);
    var d = date.getDate();
    var m = date.getMonth() + 1; //Month from 0 to 11
    var y = date.getFullYear();
    return `${d <= 9 ? '0' + d : d}/${m<=9 ? '0' + m : m}/${y}`;
}