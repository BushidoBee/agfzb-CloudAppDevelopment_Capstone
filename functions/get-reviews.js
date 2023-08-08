function main(params) {
    return new Promise(function (resolve, reject) {
      const { CloudantV1 } = require("@ibm-cloud/cloudant");
      const { IamAuthenticator } = require("ibm-cloud-sdk-core");
      const authenticator = new IamAuthenticator({
        apikey: "iZzOUZNN7534zGq2Gp3BnR35u8EXIlCNr7mXPYZ3EnpC"});
      const cloudant = CloudantV1.newInstance({authenticator: authenticator});
      cloudant.setServiceUrl("https://bbbb77a7-4b2b-4943-8232-917eac3a2199-bluemix.cloudantnosqldb.appdomain.cloud"); // TODO: Replace with your own service URL
      dealership = parseInt(params.dealerId);
      // returns dealer reviews ID
      cloudant.postFind
          ({db: "reviews",
          selector: {dealership: parseInt(params.dealerId),},}).then((result) => {
              let code = 200;
              if (result.result.docs.length == 0) {code = 404;}
              resolve({statusCode: code,headers: { "Content-Type": "application/json" },body: result.result.docs,});
        })
        .catch((err) => {reject(err);
        });
    });
  }
  
  // example invocation
  let result = main({ dealerId: 14 });
  result.then((reviews) => console.log(reviews));