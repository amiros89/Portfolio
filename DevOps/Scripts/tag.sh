#!/bin/bash
TAG="${1}/rc-${2}"
PRODUCT_DEPLOYMENT_REPO="${3}/product-deployment"
PRODUCT_SRC_REPO="${3}/${4}"

# tag PRODUCT-deployment repo
git -C $PRODUCT_DEP_REPO tag $TAG
git -C $PRODUCT_DEP_REPO push origin $TAG

git -C $PRODUCT_SRC_REPO tag $TAG
git -C $PRODUCT_SRC_REPO push origin $TAG