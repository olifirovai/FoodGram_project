const container = document.querySelector('.card-list');
const counterId = document.querySelector('#counter');
const api = new Api(apiUrl);
const header = new Header(counterId);
const configButton = {
    subscribe: {
        attr: 'data-out',
        default: {
            class: 'button_style_blue',
            text: 'Unfollow'
        },
        active: {
            class: 'button_style_blue',
            text: `Follow this author`
        }
    }
}
const subscribe = new Subscribe(configButton.subscribe, api);
const myFollow = new MyFollow(container, '.card-user', header, api, true,{
    subscribe
})
myFollow.addEvent();
