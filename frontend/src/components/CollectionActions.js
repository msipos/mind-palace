import {fetchPost} from "../utils";

class CollectionActions {
    constructor() {
        // URL where to create a collection
        this.urlNewCollection = null;

        // URL where to submit a collection action
        this.urlCollectionAction = null;

        // URL for home
        this.urlHome = null;
    }

    async submitNewCollection(name) {
        if (!this.urlNewCollection) {
            console.error("Must set urlNewCollection");
            throw {description: "Did not set urlNewCollection"};
        }
        return await fetchPost(this.urlNewCollection, {name: name});
    }

    async submitCollectionAction(action) {
        if (action !== "delete") {
            console.error("Invalid action: ", action);
            throw {description: "Invalid action", action: action};
        }

        if (!this.urlCollectionAction) {
            console.error("Must set urlCollectionAction");
            throw {description: "Did not set urlCollectionAction"};
        }

        return await fetchPost(this.urlCollectionAction, {action: action});
    }

    redirectHome() {
        if (!this.urlHome) {
            console.error("Must set urlHome");
            throw {description: "Did not set urlHome"};
        }
        window.location = this.urlHome;
    }
}

export default CollectionActions;