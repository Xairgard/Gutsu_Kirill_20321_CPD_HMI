syntax = "proto3";

package ecommerce;

service ProductInfo {
    rpc addProduct(Product) returns (ProductID);
    rpc getProduct(ProductID) returns (Product);
    rpc delProduct(ProductDel) returns (DeleteResponse); 
}

message Product {
    string id = 1;
    string name = 2;
    string description = 3;
    float price = 4;
}

message ProductID {
    string value = 1;
}

message DeleteResponse {
    bool success = 1;
    string message = 2;
}
