import {fetchPost} from "../utils";

class NoteActions {
    constructor() {
        // URL where to submit note actions
        this.urlNoteAction = null;

        // URL for note editing
        this.urlNoteEdit = null;

        // URL where to list the note's parent collection
        this.urlListCollection = null;

        // URL where to create a collection
        this.urlNewCollection = null;
    }

    async submitNoteAction(action) {
        if (action !== "delete" && action !== "archive" && action !== "unarchive") {
            console.error("Invalid action: ", action);
            throw {description: "Invalid action", action: action};
        }

        if (!this.urlNoteAction) {
            console.error("Must set urlNoteAction");
            throw {description: "Did not set urlNoteAction"};
        }

        return await fetchPost(this.urlNoteAction, {action: action});
    }

    async submitNewCollection(name) {
        if (!this.urlNewCollection) {
            console.error("Must set urlNewCollection");
            throw {description: "Did not set urlNewCollection"};
        }
        return await fetchPost(this.urlNewCollection, {name: name});
    }

    redirectToListCollection() {
        if (!this.urlListCollection) {
            console.error("Must set urlListCollection");
            throw {description: "Did not set urlListCollection"};
        }
        window.location = this.urlListCollection;
    }

    redirectToNoteEdit() {
        if (!this.urlNoteEdit) {
            console.error("Must set urlNoteEdit");
            throw {description: "Did not set urlNoteEdit"};
        }
        window.location = this.urlNoteEdit;
    }
}

export default NoteActions;