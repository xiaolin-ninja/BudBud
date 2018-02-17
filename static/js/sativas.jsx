"use strict";

class StrainsPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {strains: [], statusText: "", statusType: ""};

        this.renderTable = this.renderTable.bind(this);
        this.getMelons = this.getMelons.bind(this);
        this.sort = this.sort.bind(this);
    }

    getSativas () {
        // Get the strains via AJAX
        //
        // We could use jQuery here for our AJAX request, but it seems
        // silly to bring in all of jQuery just for one tiny part.
        // Therefore, we use the new built-into-JS "fetch" API for
        // AJAX requests. Not all browsers support this, so we have
        // a "polyfill" for it in index.html.

        this.setState({statusText: "Loading", statusType: "warning"});

        fetch("sativas.json")
            .then(r => r.json())
            .then(j => this.setState({
                melons: j.melons,
                statusText: "Loaded",
                statusType: "info",
            }));
    }

    sort (colName) {
        // Sort table by clicked on column
        this.setState({
            melons: this.state.melons.sort(
                (m1, m2) => (m1[colName] < m2[colName]) ? -1 : 1)
        });
    }

    render () {
        return (
            <div>
                <h1>Melons</h1>
                <p className="lead">Deliciousness on Demand.</p>

                <p>
                    <button className="btn btn-primary" onClick={ this.getMelons }>
                        Get Melons
                    </button>
                </p>

                <StatusBox type={ this.state.statusType } text={ this.state.statusText } />

                { this.renderTable() }
            </div>
        )
    }

    renderTable () {
        if (this.state.melons)
            return (
                <table id="MelonTable" className="table table-striped table-hover">
                    <thead>
                    <tr>
                        <th onClick={e => this.sort("type")}>
                            Type
                        </th>
                        <th onClick={e => this.sort("price")}>
                            Price
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    { this.state.melons.map(melon =>
                        <tr key={ melon.type }>
                            <td>{ melon.type }</td>
                            <td>{ melon.price }</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            )
    }
}