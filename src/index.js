function generateUI() {
    const wrapper = document.createElement('div');
    const title = document.createElement('h1');

    title.innerHTML = 'Loot Generator';

    wrapper.appendChild(title);

    return wrapper;
}

document.body.appendChild(generateUI());
