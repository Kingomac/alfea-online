class AmigoDialog extends HTMLDialogElement {
    constructor(currentUser, targetUser) {
        super();
        this.currentUser = currentUser;
        this.targetUser = targetUser;
    }

    connectedCallback() {
    }
}