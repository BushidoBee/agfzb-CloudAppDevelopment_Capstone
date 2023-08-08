function main(params) {
    return new Promise(function (resolve, reject) {
      const { CloudantV1 } = require("@ibm-cloud/cloudant");
      const { IamAuthenticator } = require("ibm-cloud-sdk-core");
      const authenticator = new IamAuthenticator({apikey: "iZzOUZNN7534zGq2Gp3BnR35u8EXIlCNr7mXPYZ3EnpC",});
      const cloudant = CloudantV1.newInstance({authenticator: authenticator,});
      cloudant.setServiceUrl("https://bbbb77a7-4b2b-4943-8232-917eac3a2199-bluemix.cloudantnosqldb.appdomain.cloud"); // TODO: Replace with your own service URL
      if (params.st) {
        // return the State of the Dealership
        cloudant.postFind({ db: "dealerships", selector: { st: params.st } })
          .then((result) => {
            let code = 200;
            if (result.result.docs.length == 0) {
              code = 404;
            }
            resolve({
              statusCode: code,
              headers: { "Content-Type": "application/json" },
              body: result.result.docs,
            });
          })
          .catch((err) => {
            reject(err);
          });
      } else if (params.dealerId) {
        id = parseInt(params.dealerId);
        // return with dealership ID
        cloudant.postFind({
            db: "dealerships",
            selector: {
              id: parseInt(params.dealerId),
            },
          })
          .then((result) => {
            let code = 200;
            if (result.result.docs.length == 0) {
              code = 404;
            }
            resolve({
              statusCode: code,
              headers: { "Content-Type": "application/json" },
              body: result.result.docs,
            });
          })
          .catch((err) => {
            reject(err);
          });
      } else {
        // All document are returned
        cloudant.postAllDocs({ db: "dealerships", includeDocs: true })
          .then((result) => {let code = 200; if (result.result.rows.length == 0) {code = 404;}
            resolve({statusCode: code, headers: { "Content-Type": "application/json" },
              body: result.result.rows,});})
          .catch((err) => {
            reject(err);
          });
      }
    });
  }
  
  let result = main({});
  result.then((dealers) => console.log(dealers));