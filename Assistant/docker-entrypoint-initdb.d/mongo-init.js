db = db.getSiblingDB("admin");
db.createUser({
  user: "userx",
  pwd: "1234",
  roles: [{ role: "readWrite", db: "admin" }],
});