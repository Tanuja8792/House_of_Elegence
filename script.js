const products = [
  {id:1,name:"Floral Printed Kurta Set",category:"Ethnic Wear",price:1899,old:2499,tag:"BESTSELLER",image:"https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=85"},
  {id:2,name:"Everyday Chic Midi Dress",category:"Dresses",price:1599,old:2199,tag:"NEW",image:"https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=700&q=85"},
  {id:3,name:"Classic White Summer Top",category:"Tops",price:899,old:1299,tag:"TRENDING",image:"https://images.unsplash.com/photo-1489602642804-64eda9c6c8c3?auto=format&fit=crop&w=700&q=85"},
  {id:4,name:"Elegant Occasion Saree",category:"Ethnic Wear",price:2799,old:3499,tag:"LIMITED EDITION",image:"https://images.unsplash.com/photo-1583391733956-6c78276477e5?auto=format&fit=crop&w=700&q=85"},
  {id:5,name:"Modern Streetwear Co-ord",category:"Western Wear",price:1999,old:2699,tag:"NEW",image:"https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=700&q=85"},
  {id:6,name:"Soft Pastel Anarkali",category:"Ethnic Wear",price:2299,old:2999,tag:"FESTIVE PICK",image:"https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=700&q=85"},
  {id:7,name:"Minimal Gold-Tone Earrings",category:"Accessories",price:499,old:799,tag:"UNDER ₹599",image:"https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=700&q=85"},
  {id:8,name:"Everyday Comfort Sneakers",category:"Footwear",price:1499,old:1999,tag:"POPULAR",image:"https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=700&q=85"},
  {id:9,name:"Elegant Black Evening Dress",category:"Dresses",price:2199,old:2899,tag:"EDITOR'S PICK",image:"https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=700&q=85"},
  {id:10,name:"Relaxed Fit Linen Shirt",category:"Tops",price:1099,old:1499,tag:"EASY DAYS",image:"https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=700&q=85"},
  {id:11,name:"Statement Heeled Sandals",category:"Footwear",price:1699,old:2299,tag:"JUST IN",image:"https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?auto=format&fit=crop&w=700&q=85"},
  {id:12,name:"Everyday Shoulder Bag",category:"Accessories",price:1299,old:1799,tag:"MOST LOVED",image:"https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=700&q=85"}
];

let activeCategory = "All";
let wishlist = new Set();
let bag = [];
let wishlistOnly = false;

const productGrid = document.getElementById("productGrid");
const resultCount = document.getElementById("resultCount");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");

function renderProducts() {
  const term = searchInput.value.trim().toLowerCase();
  const shown = products.filter(product => {
    const matchesCategory = activeCategory === "All" || product.category === activeCategory;
    const matchesSearch = (product.name + " " + product.category).toLowerCase().includes(term);
    const matchesWishlist = !wishlistOnly || wishlist.has(product.id);
    return matchesCategory && matchesSearch && matchesWishlist;
  });

  productGrid.innerHTML = shown.map(product => {
    const discount = Math.round((1 - product.price / product.old) * 100);
    return `<article class="product-card">
      <div class="product-image-wrap">
        <img class="product-image" src="${product.image}" alt="${product.name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=700&q=80'">
        <span class="product-tag">${product.tag}</span>
        <button class="wishlist-btn ${wishlist.has(product.id) ? "selected" : ""}" data-wishlist="${product.id}" aria-label="Add ${product.name} to wishlist">${wishlist.has(product.id) ? "♥" : "♡"}</button>
        <button class="add-btn" data-add="${product.id}">ADD TO BAG +</button>
      </div>
      <div class="product-info">
        <div class="product-category">${product.category}</div>
        <p class="product-name">${product.name}</p>
        <div class="product-price"><strong>₹${product.price.toLocaleString("en-IN")}</strong><span class="old-price">₹${product.old.toLocaleString("en-IN")}</span><span class="discount">${discount}% OFF</span></div>
      </div>
    </article>`;
  }).join("");

  resultCount.textContent = `${shown.length} STYLES`;
  emptyState.hidden = shown.length !== 0;
}

function setCategory(category) {
  activeCategory = category;
  wishlistOnly = false;
  document.querySelectorAll(".filter-chip").forEach(button => button.classList.toggle("active", button.dataset.filter === category));
  document.getElementById("wishlistToggle").classList.remove("is-active");
  renderProducts();
}

document.getElementById("filterList").addEventListener("click", event => {
  const button = event.target.closest("[data-filter]");
  if (button) setCategory(button.dataset.filter);
});

document.querySelectorAll(".category-tile").forEach(tile => {
  tile.addEventListener("click", () => {
    setCategory(tile.dataset.category);
    document.getElementById("shop").scrollIntoView({behavior:"smooth"});
  });
});

document.querySelectorAll("[data-nav-category]").forEach(link => {
  link.addEventListener("click", () => setCategory(link.dataset.navCategory));
});

searchInput.addEventListener("input", renderProducts);

productGrid.addEventListener("click", event => {
  const wishButton = event.target.closest("[data-wishlist]");
  const addButton = event.target.closest("[data-add]");
  if (wishButton) {
    const id = Number(wishButton.dataset.wishlist);
    wishlist.has(id) ? wishlist.delete(id) : wishlist.add(id);
    renderProducts();
  }
  if (addButton) {
    const product = products.find(item => item.id === Number(addButton.dataset.add));
    bag.push(product);
    document.getElementById("bagCount").textContent = bag.length;
    showToast(product.name + " added to your bag");
  }
});

document.getElementById("wishlistToggle").addEventListener("click", () => {
  wishlistOnly = !wishlistOnly;
  activeCategory = "All";
  document.querySelectorAll(".filter-chip").forEach(button => button.classList.toggle("active", button.dataset.filter === "All"));
  document.getElementById("wishlistToggle").classList.toggle("is-active", wishlistOnly);
  renderProducts();
  document.getElementById("shop").scrollIntoView({behavior:"smooth"});
});

document.querySelector(".bag-button").addEventListener("click", () => {
  if (!bag.length) return showToast("Your bag is waiting for something lovely!");
  showToast("Your bag has " + bag.length + (bag.length === 1 ? " item" : " items") + " · Total ₹" + bag.reduce((sum, item) => sum + item.price, 0).toLocaleString("en-IN"));
});

document.getElementById("newsletterForm").addEventListener("submit", event => {
  event.preventDefault();
  document.getElementById("newsletterMessage").textContent = "Thank you for subscribing! Welcome to the Elegance community.";
  event.target.reset();
});

document.getElementById("menuToggle").addEventListener("click", () => {
  document.querySelector(".main-nav").classList.toggle("open");
});

function showToast(message) {
  const oldToast = document.querySelector(".toast");
  if (oldToast) oldToast.remove();
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);
  window.setTimeout(() => toast.remove(), 2400);
}

renderProducts();
